Here we are going to implement an automated chatting system exclusively for our website using OpenAI. Our new system will answer questions with natural language as ChatGPT use. The new system will answer from our website content.

To achieve this, we need to train OpenAI with our website data. So, are going to crawl our website first to get the data, then we will pass those data OpenAI API to train. This API will return some formatted data that we will save as processed data. When user ask any question, we will pass this processed data to OpenAI API and that API process that data to prepare answer.
So we have three part of our program, they are -
1. Crawl: to get data from website for train
2. Prepare: to prepare those data ans save the prepared data as processed data to use in future
3. Ask: to get answer of user’s question

I marge 1 & 2 into one file and quirying OpenAI into 3rd file. We will use docker to package our python program. So, we can easily maintain our program.

Before start to code we need to prepare ourself. Like we need a simple website that we are going to crawl. I prepared a website for this purpose and host it into my personal server. Please note, the prescribed Python program from OpenAI use HTTPS to crawl. So, I host that under my HTTPS enabled server which is https://site4chatgptrnd.shahadathossain.com/ the source code of this website I put into “public_html” folder of my github repository.

Another thing we need to do is to setup an OpenAI API Key by visiting https://platform.openai.com/docs/api-reference/introduction or https://platform.openai.com/account/api-keys [through your signed in account > API Keys link] Please note, you need to spend a small amount of money like $5.00 to get access of OpenAI for three months.

We can interact with the API through HTTP requests from any language, via OpenAI’s official Python bindings, OpenAI’s official Node.js library, or a community-maintained library. I’m Python fan, so I’ll use Python bindings. As I packaged into docker, so "Docker" file take care installation / setup process. To run build docker and run docker you can use these code -
```
sudo docker build -t openai2test .
sudo docker run -d --network=host openai2test:latest
```

As I told we need another server for static content from which our chat program answer the query of our user. I use here apache server with PHP. User ask question to PHP through Apache server and PHP communicate with underlaying Python server which is run by docker and send response to end user through Apache server. Our PHP code and static website hosted under "public_html" file.

Now we are ready to run prescribed code of OpenAI. We already build and execute our docker and it will communicate through 50024 port at localhost.
