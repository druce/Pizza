FROM ubuntu:18.04

MAINTAINER Druce Vertes "drucev@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN pip3 install --upgrade pip

# Copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

COPY apikeys /app/apikeys

EXPOSE 8181

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]



