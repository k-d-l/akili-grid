FROM python:3.9-buster

WORKDIR /app
COPY . . 

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
CMD ["help"]