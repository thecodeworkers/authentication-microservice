FROM python:3.8-alpine

RUN mkdir /usr/app
WORKDIR /usr/app
RUN apk add g++ linux-headers libffi-dev openssl openssl-dev
COPY ./requirements.txt /usr/app
VOLUME [ "/usr/app" ]
RUN pip install -r requirements.txt
CMD python run.py
