FROM python:3.10
WORKDIR /code
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install -U setuptools
RUN pip install -r requirements.txt
COPY src/ .
RUN python crawl-and-train.py
CMD ["python", "./ask.py"]
