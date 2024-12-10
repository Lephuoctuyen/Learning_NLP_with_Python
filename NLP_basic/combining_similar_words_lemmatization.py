from nltk.stem import WordNetLemmatizer
import time
import nltk
import spacy
nltk.download('wordnet')
nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger') # Run the first time you run the notebook
nlp = spacy.load('en_core_web_sm')

def read_text_file(filename):
	file = open(filename,'r', encoding='utf-8')
	return file.read()


def preprocess_text(text):
	text = text.replace('\n','')
	return text 


# dividing sentences into words 
def tokenize_nltk(text):
	sentences = nltk.tokenize.word_tokenize(text)
	return sentences

def tokenize_spacy(text):
	doc = nlp(text)
	return [sentence.text for sentence in doc]

def pos_tag_spacy(text, model):
	doc = model(text)
	words = [token.text for token in doc]
	pos = [token.pos_ for token in doc]
	return list(zip(words, pos))

def pos_tag_nltk(text):
	words = tokenize_nltk(text)
	words_with_pos = nltk.pos_tag(words)
	return words_with_pos

def main():
    file = 'data.txt'
    text = read_text_file(file)
    text = preprocess_text(text)
    start = time.time()
    pos_tag = pos_tag_nltk(text)
    print(pos_tag)
    print(f"NLTK: {time.time() - start} s")

    start = time.time()
    pos_tag = pos_tag_spacy(text, nlp)
    print(f"spaCy: {time.time() - start} s")
	
lemmatizer = WordNetLemmatizer()
pos_mapping = {
    "JJ": "a",
    "JJR": "a",
    "JJS": "a",
    "NN": "n",
    "NNS": "n",
    "VBD": "v",
    "VBG": "v",
    "VBN": "v",
    "VBP": "v",
    "VBZ": "v",
}
accepted_pos = {"a", "v", "n"}


def lemmatize(words):
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words


def lemmatize_long_text(text):
    words = pos_tag_nltk(text)
    words1 = [
        (
            word_tuple[0],
            pos_mapping[word_tuple[1]]
            if word_tuple[1] in pos_mapping.keys()
            else word_tuple[1],
        )
        for word_tuple in words
    ]
    words = [
        (
            lemmatizer.lemmatize(word_tuple[0],word_tuple[1])
            if word_tuple[1] in accepted_pos
            else word_tuple[0],
            word_tuple[1],
        )
        for word_tuple in words1
    ]
    return words1,words


def main():
    words = ["leaf", "leaves", "booking", "writing", "completed", "stemming"]
    lem_words = lemmatize(words)
    lem_words.append(lemmatizer.lemmatize("loved", "v"))
    lem_words.append(lemmatizer.lemmatize("worse", "a"))
    print(lem_words)
    sherlock_holmes_text = read_text_file("/content/sherlock_holmes_1.txt")
    lem_words1,lem_words = lemmatize_long_text(sherlock_holmes_text)
    print(lem_words)
    print(lem_words1)
