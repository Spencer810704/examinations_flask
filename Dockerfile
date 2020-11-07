FROM python:3.6
LABEL maintainer="spencer810704@gmail.com"
RUN mkdir /app
WORKDIR /app
COPY ./app /app 
RUN chmod +x /app/wait-for-it.sh
RUN apt-get update && apt-get install -y vim lsof
RUN pip3 install -r requirements.txt
