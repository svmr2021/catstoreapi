FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
#RUN mkdir /code/staticfiles
#RUN mkdir /code/mediafiles
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /code/
