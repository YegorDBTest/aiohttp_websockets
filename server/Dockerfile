FROM python:3.8.3

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r /tmp/requirements.txt

ADD . /app
WORKDIR /app

EXPOSE 8000
