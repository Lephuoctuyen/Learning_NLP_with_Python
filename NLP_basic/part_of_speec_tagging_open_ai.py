from openai import OpenAI
import instructor
from pydantic import BaseModel, Field

client = OpenAI(api_key='OPEN_AI_KEY',
                                              base_url="https://api.chatanywhere.tech/v1")
client = instructor.from_openai(client)

class Format(BaseModel):
  result : list[(str)] 


def pos_tag_gpt(prompt : str):
  return client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {"role": "system", "content": "You are a helpful assistant in field parts of speech tagging."},
            {"role": "user", "content": prompt}
    ],
    response_model=Format,)
  
text = 'In his eyes she eclipses and predominates the whole of her sex.'
prompt = f"""Decide what the part of speech tags are for a sentence. 
    Preserve original capitalization. 
    Return the list in the format of a python tuple: (word, part of speech).
    Do not include any other explanations.
    Sentence: {text}."""
response = pos_tag_gpt(prompt)


########################################### 

from ast import literal_eval

def pos_tag_gpt(text, client):
    prompt = f"""Decide what the part of speech tags are for a sentence. 
    Preserve original capitalization. 
    Return the list in the format of a python tuple: (word, part of speech).
    Do not include any other explanations.
    Sentence: {text}."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],    
    )
    result = response.choices[0].message.content
    result = result.replace("\n", "")
    result = list(literal_eval(result))
    return result

    import time
start = time.time()
first_sentence = "In his eyes she eclipses and predominates the whole of her sex."
words_with_pos = pos_tag_gpt(first_sentence, client)
print(words_with_pos)
print(f"GPT: {time.time() - start} s")