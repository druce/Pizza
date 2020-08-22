#!/bin/zsh
# run app server in container
# build container
docker build . -t pizza
docker run -p 8181:8181 --name pizza --rm pizza &

# or just run local app
# python app.py

# run local dev webserver
# npm lite

# run dev webserver plus watch for changes to js, scss
npm start

# or just open the index.html in browser
# IP address for app server is in js/main.js
