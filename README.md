Here we are going to implement an automated chatting system exclusively for our website using OpenAI. Our new system will answer questions with natural language as ChatGPT use. The new system will answer from our website content.

To achieve this, we need to train OpenAI with our website data. So, are going to crawl our website first to get the data, then we will pass those data OpenAI API to train. This API will return some formatted data that we will save as processed data. When user ask any question, we will pass this processed data to OpenAI API and that API process that data to prepare answer.
So we have three part of our program, they are -
1. Crawl: to get data from website for train
2. Prepare: to prepare those data ans save the prepared data as processed data to use in future
3. Ask: to get answer of user’s question

Before start to code we need to prepare ourself. Like we need a simple website that we are going to crawl. I prepared a website for this purpose and host it into my personal server. Please note, the prescribed Python program from OpenAI use HTTPS to crawl. So, I host that under my HTTPS enabled server which is https://www.shahadathossain.com/site4chatgptrnd/ the source code of this website I put into “website2crawl” folder of my github repository. Please find github repository link at the end of this document.

Another thing we need to do is to setup an OpenAI API Key by visiting https://platform.openai.com/docs/api-reference/introduction or https://platform.openai.com/account/api-keys [through your signed in account > API Keys link] Please note, you need to spend a small amount of money like $5.00 to get access of OpenAI for three months.

We can interact with the API through HTTP requests from any language, via OpenAI’s official Python bindings, OpenAI’s official Node.js library, or a community-maintained library. I’m Python fan, so I’ll use Python bindings. To install the official Python bindings, run the following command:
  sudo apt update
  sudo apt upgrade
  sudo python3 -m pip install --upgrade pip
  sudo apt install python3-pip python3-setuptools python3.x-venv
  python3 -m venv webcrawler
  cd webcrawler
  source bin/activate
  >>>>> put “src” folder’s code into “webcrawler” folder
  pip3 install -r requirements.txt

Above code I install virtual environment and activate it. Please note, I use version 3.10 like “python3.10-venv” as my python version is 3.10. So, check your version and change the above command accordingly.

Now we are ready to run prescribed code of OpenAI. First we execute “crawl.py” to crawl our website to get data and then “prepare.py” to prepare our data for OpenAI and finally execute “ask.py” where user can ask question.
