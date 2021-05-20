FROM python:3.7

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
COPY ./challenge.py /usr/src/app/
RUN pip3 install -r requirements.txt
