import time
import nltk
import spacy

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
	