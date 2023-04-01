Here we are going to implement an automated chatting system exclusively for our website using OpenAI. Our new system will answer questions with natural language as ChatGPT use. The new system will answer from our website content.

To achieve this, we need to train OpenAI with our website data. So, are going to crawl our website first to get the data, then we will pass those data OpenAI API to train. This API will return some formatted data that we will save as processed data. When user ask any question, we will pass this processed data to OpenAI API and that API process that data to prepare answer. So we have three part of our program, they are -

1. Crawl: to get data from website for train
2. Prepare: to prepare those data ans save the prepared data as processed data to use in future
3. Ask: to get answer of user’s question

I marge 1 & 2 into one file and quirying OpenAI into 3rd file. We will use docker to package our python program. So, we can easily maintain our program. To dockerize our program we need to follow these steps -

1. Install docker (it’s one time task, if docker installed into system, we can ignore this step)
2. Create our docker file where necessary steps will written, so docker will read that file and execute that file sequentially while building our image.
3. Create a requirement file for the project which already prescribed by OpenAI. I add some more module like Flask and other for extra work at the end of file.
4. Build our image by “docker build” command (I’ll write full command to build image later of this document)
5. Run or execute our newly created image (this command also documented here, later)

Also we need to prepare our static website from which OpenAI will find the answer. For this purpose I create a static site and host it with this project. So, we first need to execute this project and we will get that static site. After that we will execute our training code, so that training code will get our static site. So, we will run our program first, then execute program to train, then we can ask question.

For this project we have another challenge, we use HTTPS while crawling. So, I need to host it with SSL. Here I use Let’s encrypt free SSL to achieve this. As we using micro-server, we need “standalone” SSL.
```
$ sudo certbot certonly --standalone -d site4chatgptrnd.shahadathossain.com
```
Note: Before execute above code we need to ensure that 80 and 443 port is not bind with the domain.

When it run successfully, it provide all necessary certificate files. In my server the location of those files was “/etc/letsencrypt/live/site4chatgptrnd.shahadathossain.com/” Now, we need to copy “cert.pem”, “privkey.pem” and “fullchain.pem” into our “\<project-root\>/pure-python-version/ssl-certificates/” directory. To do this, we can apply following commands -
```
$ sudo cp /etc/letsencrypt/live/site4chatgptrnd.shahadathossain.com/fullchain.pem pure-python-version/ssl-certificates/
$ sudo cp /etc/letsencrypt/live/site4chatgptrnd.shahadathossain.com/cert.pem pure-python-version/ssl-certificates/
$ sudo cp /etc/letsencrypt/live/site4chatgptrnd.shahadathossain.com/privkey.pem pure-python-version/ssl-certificates/
```
Note: Symbolic-link or hard-link will not work here in Docker.

As we encapsulate our code into Docker, our challenge is how we point the certificates with our Docker file system. We can create volume and point that folder. But, I can’t did it successfully. So, I do another way, which is copy the certificates each time docker image build. So, problem is, I need to rebuild our image each time SSL certificates need to renew. Also after renew SSL certificate, we need to execute above copy commands.

Another thing we need to do is to setup an OpenAI API Key by visiting https://platform.openai.com/docs/api-reference/introduction or https://platform.openai.com/account/api-keys [through your signed in account > API Keys link] Please note, you need to spend a small amount of money like $5.00 to get access of OpenAI for three months.

We can interact with the API through HTTP requests from any language, via OpenAI’s official Python bindings, OpenAI’s official Node.js library, or a community-maintained library. I’m Python fan, so I’ll use Python bindings. As I packaged into docker, so "Docker" file take care installation / setup process. I just add a line into “Docker” file that we are going to use python with version. So docker will download python image from internet and embed that python into our project.

In Docker build there has several argument we can pass while building image that help to configure our required data like API key, server host and port etc.

To run build docker and run docker you can use these code -
```
$ sudo docker build --build-arg OPENAI_KEY=secret-api-key -t openaiusingpurepython .
$ sudo docker run -d --name openaiusingpurepython_container --network=host openaiusingpurepython:latest
```
Note: By default, our program will run 59014 port. We can change port while running docker by following argument -
```
$ sudo docker run -d --name openaiusingpurepython_container --network=host openaiusingpurepython:latest 59876
```
Here we run our code with custom port 59876.

Here is another sample by which your code will execute at local server (localhost without SSL) but it get data from remote server -
```
$ sudo docker build --build-arg OPENAI_KEY=secret-api-key --build-arg SERVER_HOST=localhost --build-arg SERVER_SSL=0 --build-arg CRAWL_ROOT="https://site4chatgptrnd.shahadathossain.com:59014/" -t openaiusingpurepython .
```

Please note, we need to allow our port into OS firewall. In ubuntu we can apply following commands -
```
$ sudo ufw allow 59014/tcp
$ sudo ufw reload
```
After running docker, we need to crawl our project and execute learning session of AI before try to getting answer from our system. We need to invoke following commands into our running container -
```
$ sudo docker exec -it openaiusingpurepython_container python ./crawl-and-train.py
```
Now we are ready to run see the result! We already build and execute our docker and it will communicate through 59014 port.

## Demo https://site4chatgptrnd.shahadathossain.com:59014/
