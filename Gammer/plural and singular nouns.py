## Counting nouns – plural and singular nouns

import nltk
from nltk.stem import WordNetLemmatizer
import inflect
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from NLP_basic.pos_tagging import pos_tag_nltk

def read_text_file(filename):
    file = open(filename, "r", encoding="utf-8") 
    return file.read()

def preprocess_text(text):
    text = text.replace("\n", " ")
    return text

def is_plural_wn(noun):
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(noun, 'n')
    print(lemma)
    plural = True if noun is not lemma else False
    return plural

def is_singular_wn(noun):
    return not is_plural_wn(noun)
    
def is_plural_nltk(noun_info):
    pos = noun_info[1]
    if (pos == "NNS"):
        return True
    else:
        return False

def is_singular_nltk(noun_info):
    pos = noun_info[1]
    if (pos == "NN"):
        return True
    else:
        return False

def get_plural(singular_noun):
    p = inflect.engine()
    return p.plural(singular_noun)
    
def get_singular(plural_noun):
    p = inflect.engine()
    plural = p.singular_noun(plural_noun)
    if (plural):
        return plural
    else:
        return plural_noun

def get_nouns(words_with_pos):
    noun_set = ["NN", "NNS"]
    nouns = [word for word in words_with_pos if word[1] in noun_set]
    return nouns

def plurals_wn(words_with_pos):
    other_nouns = []
    for noun_info in words_with_pos:
        word = noun_info[0]
        plural = is_plural_wn(word)
        if (plural):
            singular = get_singular(word)
            other_nouns.append(singular)
        else:
            plural = get_plural(word)
            other_nouns.append(plural)
    return other_nouns

def plurals_nltk(nouns):
    other_nouns = []
    for noun_info in nouns:
        word = noun_info[0]
        pos = noun_info[1]
        if (pos == "NNS"):
            singular = get_singular(noun_info[0])
            other_nouns.append(singular)
        else:
            plural = get_plural(noun_info[0])
            other_nouns.append(plural)
    return other_nouns

def main():
    sherlock_holmes_text = read_text_file("Chapter01/sherlock_holmes_1.txt")
    sherlock_holmes_text = preprocess_text(sherlock_holmes_text)
    words_with_pos = pos_tag_nltk(sherlock_holmes_text)
    nouns = get_nouns(words_with_pos)
    print(nouns)
    #other_nouns_wn = plurals_wn(nouns)
    #print(other_nouns_wn)
    #other_nouns_nltk = plurals_nltk(nouns)
    #print(other_nouns_nltk)
    #print(is_plural_wn("men"))
    word_info = pos_tag_nltk("men")
    print(word_info)



if (__name__ == "__main__"):
    main()

### Basic method: spaCy lemma versus spaCy token
"""

import spacy
nlp = spacy.load('en_core_web_sm')
text = 'I have five birds'
doc = nlp(text)
for token in doc:
  print(token.lemma_)
  if (token.pos_ == 'NOUN' and token.lemma_ != token.text):
    print(token.text, 'plural')

import spacy
nlp = spacy.load('en_core_web_sm')
words = ["leaf", "leaves", "books", "writing", "completed", "stemming"]
docs = [nlp(word) for word in words]
for doc in docs:
    for token in doc:
        print(token, token.lemma_)

"""### Number using morph features

"""

doc = nlp(text)
print(doc[3].morph.get("Number"))

from enum import Enum

class Noun_number(Enum):
  SINGULAR = 1
  PLURAL = 2

def get_nouns_number(text, model, method='lemma'):
  nouns = []
  doc = model(text)
  for token in doc:
    if (token.pos_ == 'NOUN'):
      if method == 'lemma':
        if token.lemma_ != token.text:
            nouns.append((token.text, Noun_number.PLURAL))
        else:
            nouns.append((token.text, Noun_number.SINGULAR))
      elif method == 'morph':
        if token.morph.get("Number") == "sing":
            nouns.append((token.text, Noun_number.PLURAL))
        else:
            nouns.append((token.text, Noun_number.SINGULAR))
  return nouns

text = "Three geeses crossed the road"
nouns = get_nouns_number(text, nlp, "morph")
print(nouns)
nouns = get_nouns_number(text, nlp)
print(nouns)

"""### Noun number using GPT-3

"""

import instructor
from pydantic import BaseModel, Field

client = OpenAI(api_key='sk-RYiDonFCU85Bfr242X2POvCBhlhfHlz8knZQoVjWVJw180s6',
                                              base_url="https://api.chatanywhere.tech/v1")
client = instructor.from_openai(client)

class Format(BaseModel):
  result : (str)


def pos_tag_gpt(prompt : str):
  return client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {"role": "system", "content": "You are a helpful assistant ."},
            {"role": "user", "content": prompt}
    ],
    response_model=Format,)
prompt="""Decide whether each noun in the following text is singular or plural.
Return the list in the format of a python tuple: (word, number). Do not provide any additional explanations.
Sentence: Three geese crossed the road."""

response = pos_tag_gpt(prompt)
response.result

"""### Converting from singular to plural and plural to singular



"""

from textblob import TextBlob
import nltk
nltk.download('punkt_tab')
texts = ['book','goose','pen','point','deer']
blob_objs = [TextBlob(text) for text in texts]
plurals = [blob.words[0].pluralize() for blob in blob_objs]
print(plurals)
blob_objs = [TextBlob(text) for text in plurals]
singles = [blob.words[0].singularize() for blob in blob_objs]
print(singles)

