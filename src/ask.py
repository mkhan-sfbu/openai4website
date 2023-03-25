from flask import Flask, request, jsonify, json
################################################################################
### Step 1
################################################################################

import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import pandas as pd
import tiktoken
import openai
import numpy as np
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity

openai.organization = ''
openai.api_key = ''

# Regex pattern to match a URL
HTTP_URL_PATTERN = r'^http[s]*://.+'

# Define root domain to crawl
domain = 'site4chatgptrnd.shahadathossain.com'



################################################################################
### Step 11
################################################################################

df=pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

df.head()

################################################################################
### Step 12
################################################################################

def create_context(
    question, df, max_len=1800, size="ada"
):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')


    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        
        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4
        
        # If the context is too long, break
        if cur_len > max_len:
            break
        
        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)

def answer_question(
    df,
    model="text-davinci-003",
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the questin and context
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""

################################################################################
### Step 13
################################################################################

#print(answer_question(df, question="What day is it?", debug=False))

#print(answer_question(df, question="What is our newest embeddings model?"))

#print(answer_question(df, question="When Gregory Anderson was fired?"))
#print(answer_question(df, question="Who are the founder of Yahoo?"))

'''
print('Ask question, like "When Gregory Anderson was fired?" [without quote]')
qAsked=''
while qAsked != 'quit':
    qAsked=input('Please ask question about Yahoo, or enter quit: ')
    if qAsked != 'quit':
        print(answer_question(df, question=qAsked))

print('........... thank you ...........')
'''



####################################################################
### Stemp 14
################################################################
# Define the server address and port
host = 'localhost'
port = 50024 # 500AI
print(f"Serving at http://{host}:{port}")

app = Flask(__name__)
@app.route('/', methods=['POST'])
def responseToQuestion():
    response = {
            'status': 400
        }
    if request.method == 'POST':
        data=request.get_json()
        if data.get("question") == "":
            return jsonify(response)
        response = {
            'question': data.get("question"),
            'answer': answer_question(df, question=data.get("question")),
            'status': 200
        }
        # '''
    
    # Return the response as JSON
    return jsonify(response)

# Start the Flask app
if __name__ == '__main__':
    app.run(port=port, host=host)


