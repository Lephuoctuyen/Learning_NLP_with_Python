import time
import nltk
import spacy

nltk.download('punkt')
# tokenizer = nltk.data.load('tokenizer/punkt/english.pickle')
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

def main():
	file = 'data.txt'
	text = read_text_file(file)
	words_nltk = tokenize_nltk(text)
	words_spacy = tokenize_spacy(text)
