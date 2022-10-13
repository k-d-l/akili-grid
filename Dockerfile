from python:3.9-buster

WORKDIR /app
COPY . . 

RUN pip install -r requirements.txt

ENTRYPOINT ['/usr/local/bin/python', 'main.py']
CMD ['help']