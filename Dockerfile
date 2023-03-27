FROM python:3.10
WORKDIR /code
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install -U setuptools
RUN pip install -r requirements.txt
ARG OPENAI_KEY=xxx
ARG SERVER_HOST=python.site4chatgptrnd.shahadathossain.com
ARG SERVER_PORT=59014
#ARG CRAWL_DOMAIN=python.site4chatgptrnd.shahadathossain.com
ARG CRAWL_ROOT=
COPY pure-python-version/ /code/
RUN ls -la /code/*
RUN touch /code/env.txt
RUN printenv > /code/env.txt
RUN python process.env.py
ENTRYPOINT ["python", "ask.py"]
# RUN python crawl-and-train.py
