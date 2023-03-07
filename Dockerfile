FROM python:3.10-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./Backend_iSi/ .

RUN python manage.py makemigrations && python manage.py migrate
RUN python manage.py loaddata chat

EXPOSE 8000