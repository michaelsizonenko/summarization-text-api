FROM python:3.9
WORKDIR /summarization
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip install --no-cache-dir --upgrade -r /summarization/requirements.txt
RUN python -m nltk.downloader stopwords

EXPOSE 8000

