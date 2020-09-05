FROM python:3.7.2-slim
MAINTAINER Druce Vertes "drucev@gmail.com"

# Copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app
COPY apikeys /app/apikeys

EXPOSE 8181
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]



