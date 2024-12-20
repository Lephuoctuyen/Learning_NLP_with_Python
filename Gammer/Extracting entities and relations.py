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



###################



import spacy
import textacy

nlp = spacy.load('en_core_web_sm')
sentences = ["All living things are made of cells.", "Cells have organelles."]

verb_patterns = [[{"POS":"AUX"}, {"POS":"VERB"}, {"POS":"ADP"}], [{"POS":"AUX"}]]

def contains_root(verb_phrase, root):
    vp_start = verb_phrase.start
    vp_end = verb_phrase.end
    if (root.i >= vp_start and root.i <= vp_end):
        return True
    else:
        return False

def get_verb_phrases(doc):
    root = find_root_of_sentence(doc)
    # Changed the line below to use token_matches instead of matches
    verb_phrases = list(textacy.extract.token_matches(doc, verb_patterns))
    new_vps = []
    for verb_phrase in verb_phrases:
        if contains_root(verb_phrase, root):
            new_vps.append(verb_phrase)
    return new_vps

def longer_verb_phrase(verb_phrases):
    longest_length = 0
    longest_verb_phrase = None
    for verb_phrase in verb_phrases:
        if len(verb_phrase) > longest_length:
            longest_verb_phrase = verb_phrase
    return longest_verb_phrase

def find_noun_phrase(verb_phrase, noun_phrases, side):
    for noun_phrase in noun_phrases:
        if (side == "left" and noun_phrase.start < verb_phrase.start):
            return noun_phrase
        elif (side == "right" and noun_phrase.start > verb_phrase.start):
            return noun_phrase

def find_triplet(sentence):
    doc = nlp(sentence)
    verb_phrases = list(get_verb_phrases(doc))
    noun_phrases = doc.noun_chunks

    # Handle the case where no verb phrases are found
    if not verb_phrases:
        return (None, None, None)  # Or raise an exception, or handle it differently

    verb_phrase = longer_verb_phrase(verb_phrases) if len(verb_phrases) > 1 else verb_phrases[0]
    left_noun_phrase = find_noun_phrase(verb_phrase, noun_phrases, "left")
    right_noun_phrase = find_noun_phrase(verb_phrase, noun_phrases, "right")
    return (left_noun_phrase, verb_phrase, right_noun_phrase)

def main():
    for sentence in sentences:
        (left_np, vp, right_np) = find_triplet(sentence)
        print(left_np, "\t", vp, "\t", right_np)


main()