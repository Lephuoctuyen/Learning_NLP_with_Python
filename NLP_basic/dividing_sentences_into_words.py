import time
import nltk
import spacy

tokenizer = nltk.data.load('tokenizer/punkt/english.pickle')
nlp = spacy.load('en_core_web_sm')

def read_text_file(filename):
	file = open(file,'r', encoding='utf-8')
	return file.read()


def preprocess_text(text):
	text = text.replace('\n','')
	return text 


# dividing sentences into words 
def tokenize_nltk(text):
	sentences = tokenizer.tokenize(text)
	return sentences

def tokenize_spacy(text):
	doc = nlp(text)
	return [sentence.text for sentence in doc]

def main():
	file = 'data.txt'
	text = read_text_file(file)
	words_nltk = tokenize_nltk(text)
	words_spacy = divide_into_sentences_spacy(text)
	