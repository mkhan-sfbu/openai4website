FROM python:3.10
WORKDIR /code
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install -U setuptools
RUN pip install -r requirements.txt
ARG OPENAI_KEY=null
ARG SERVER_HOST=null
ARG SERVER_PORT=null
ARG SERVER_SSL=null
ARG CRAWL_ROOT=null
COPY pure-python-version/ /code/
RUN ls -la /code/*
RUN touch /code/env.txt
RUN printenv > /code/env.txt
RUN python process.env.py
ENTRYPOINT ["python", "ask.py"]
# RUN python crawl-and-train.py
