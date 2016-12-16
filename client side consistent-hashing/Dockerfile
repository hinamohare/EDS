FROM python:3.5.2

#This is explanation about the application owner
MAINTAINER Hina Mohare "heenamohare@gmail.com"

#copies the files in current folder to /code in the container
COPY . /code

#This sets the working directory as /code
WORKDIR /code/

#These instructions install all the required dependencies for this instruction
RUN pip install	configparser
RUN pip install	pymysql
RUN pip install	flask
RUN pip install	flask-sqlalchemy
RUN pip install	flask-wtf
RUN pip install	sqlalchemy
RUN pip install	Flask-Script
RUN pip install	Flask-Migrate
RUN pip install	simplejson

#This exposes the port 5000 for the connection at the host machine
EXPOSE 5000
