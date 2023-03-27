from flask import Flask, request, jsonify, json, render_template, send_from_directory
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

import ssl
from settings import config, toConfig, getConfigAfterChangingData
import sys


cnfg = config()

if 'org' in cnfg['openai']:
    openai.organization = cnfg['openai']['org']
openai.api_key = cnfg['openai']['key']

# Regex pattern to match a URL
HTTP_URL_PATTERN = r'^http[s]*://.+'

# Define root domain to crawl
# domain = 'site4chatgptrnd.shahadathossain.com'
# domain = cnfg['crawl']['domain']



################################################################################
### Step 11
################################################################################
def getDf():
    df=pd.read_csv('processed/embeddings.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
    df.head()
    return df

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
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
ctx.load_verify_locations('ssl-certificates/fullchain.pem')
ctx.load_cert_chain('ssl-certificates/cert.pem', 'ssl-certificates/privkey.pem')

# Define the server address and port
host = cnfg['server']['host']
port = cnfg['server']['port'] # 500AI
print(f"Serving at https://{host}:{port}")

app = Flask(__name__, template_folder='templates')
@app.route('/', methods=['POST', 'GET'])
def responseToQuestion():
    response = {
            'status': 400
        }
    if request.method == 'POST':
        data=request.form
        if data.get("question") == "":
            return jsonify(response)
        response = {
            'question': data.get("question"),
            'answer': answer_question(getDf(), question=data.get("question")),
            'status': 200
        }
    if request.method == 'GET':
        return render_template('index.htm')

    
    # Return the response as JSON
    return jsonify(response)

@app.route('/<string:htmlfile>', methods=['GET'])
def sendContent(htmlfile):
    response = {
            'status': 400
        }
    if request.method == 'GET':
        return render_template(htmlfile+'.htm')
    # Return the response as JSON
    return jsonify(response)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Start the Flask app
if __name__ == '__main__':
    '''
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>1}: {arg}")
    '''
    if len(sys.argv)>1 and int(sys.argv[1])>0 and port!=int(sys.argv[1]):
        port=int(sys.argv[1])
        nData=getConfigAfterChangingData(cnfg, port, 'server', 'port')
        if nData[0]==True:
            print('New port: '+str(port))
            toConfig(nData[1])
            print('Port update into config file - DONE')
    app.run(port=port, host=host, ssl_context=ctx)


