# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /python-docker-g3

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5500"]