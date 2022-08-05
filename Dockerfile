FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r env/requirements.txt
ENV PYTHONUNBUFFERED=0

EXPOSE 80

 CMD ["gunicorn", "app:application", "--config=env/gunicorn_config.py"]