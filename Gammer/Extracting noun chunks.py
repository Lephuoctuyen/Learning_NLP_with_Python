import spacy

nlp = spacy.load('en_core_web_sm')
def print_noun_chunks(sentence, model):
  doc = model(sentence)
  for chunk in doc.noun_chunks:
    print(chunk.text)


sentences = """To Sherlock Holmes she is always _the_ woman. I have seldom heard him mention her under any other name. In his eyes she eclipses and predominates the whole of her sex. It was not that he felt any emotion akin to love for Irene Adler. All emotions, and that one particularly,
were abhorrent to his cold, precise but admirably balanced mind. He
was, I take it, the most perfect reasoning and observing machine that
the world has seen, but as a lover he would have placed himself in a
false position. He never spoke of the softer passions, save with a gibe
and a sneer. They were admirable things for the observer—excellent for
drawing the veil from men’s motives and actions. But for the trained
reasoner to admit such intrusions into his own delicate and finely
adjusted temperament was to introduce a distracting factor which might
throw a doubt upon all his mental results. Grit in a sensitive
instrument, or a crack in one of his own high-power lenses, would not
be more disturbing than a strong emotion in a nature such as his. And
yet there was but one woman to him, and that woman was the late Irene
Adler, of dubious and questionable memory."""
print_noun_chunks(sentences, nlp)

def explore_properties(sentence, model):
  doc = model(sentence)
  other_span = 'emotions'
  other_doc = model(other_span)
  for noun_chunk in doc.noun_chunks:
    print(noun_chunk.text)
    print("Noun chunk start and end", "\t", noun_chunk.start, "\t", noun_chunk.end)
    print("Noun chunk sentence:", noun_chunk.sent)
    print("Noun chunk root:", noun_chunk.root.text)
    print(f"Noun chunk similarity to '{other_span}'", noun_chunk.similarity(other_doc))
    print(f"Similarity of the sentence '{sentence}' to '{other_span}':", doc.similarity(other_doc))


sentence = "All emotions, and that one particularly, were abhorrent to his cold, precise but admirably balanced mind."
explore_properties(sentence, nlp)


import spacy

compound_sentence = "He eats cheese, but he won’t eat ice cream."
complex_sentence = "If it rains later, we won't be able to go to the park."
nlp = spacy.load('en_core_web_sm')

verb_pos_set = ["VERB"]

# để tìm token có thẻ ROOT.
def find_root_of_sentence(doc):
    root_token = None
    for token in doc:
        if (token.dep_ == "ROOT"):
            root_token = token
    return root_token

def find_other_verbs(doc, root_token):
    other_verbs = []
    for token in doc:
        ancestors = list(token.ancestors)
        if (token.pos_ == "VERB" and len(ancestors) == 1 and ancestors[0] == root_token):
            other_verbs.append(token)
    return other_verbs

def get_clause_token_span_for_verb(verb, doc, all_verbs):
    first_token_index = len(doc)
    last_token_index = 0
    this_verb_children = list(verb.children)
    for child in this_verb_children:
        if (child not in all_verbs):
            if (child.i < first_token_index):
                first_token_index = child.i
            if (child.i > last_token_index):
                last_token_index = child.i

    return(first_token_index, last_token_index)

def potential_clause_contains_subj(clause):
    contains_subj = False
    for token in clause:
        if (token.dep_ == "nsubj"):
            contains_subj = True
    return contains_subj

def print_doc_info(doc):
    for token in doc:
        ancestors = [t.text for t in token.ancestors]
        children = [t.text for t in token.children]
        print(token.text, "\t", token.i, "\t", token.pos_, "\t", token.dep_, "\t", ancestors, "\t", children)

def get_clauses(sentence):
    doc = nlp(sentence)
    print_doc_info(doc)
    # Find the root token
    root_token = find_root_of_sentence(doc)
    print(root_token)
    # Find the other verbs
    other_verbs = find_other_verbs(doc, root_token)
    print(other_verbs)
    token_spans = []
    # Find the token span for each of the other verbs
    all_verbs = [root_token] + other_verbs
    for other_verb in all_verbs:
        (first_token_index, last_token_index) = get_clause_token_span_for_verb(other_verb, doc, all_verbs)
        token_spans.append((first_token_index, last_token_index))
    sentence_clauses = []
    print(token_spans)
    is_CCONJ = False
    for token in doc:
        if (token.pos_ == "CCONJ"):
            is_CCONJ = True

    for i, token_span in enumerate(token_spans):
        start, end = token_span
        if i > 0 and is_CCONJ:
            start -= 1
        if start < end:
            clause = doc[start:end]
            if potential_clause_contains_subj(clause):
                sentence_clauses.append(clause)

    sentence_clauses = sorted(sentence_clauses, key=lambda tup: tup[0])
    return sentence_clauses

def main():
    # clauses = get_clauses(complex_sentence)
    # clauses_text = [clause.text for clause in clauses]
    # print(clauses_text)
    clauses = get_clauses(compound_sentence)
    clauses_text = [clause.text for clause in clauses]
    print(clauses_text)


if (__name__ == "__main__"):
    main()