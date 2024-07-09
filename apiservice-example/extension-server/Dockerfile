FROM python:3.9

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 443

CMD ["python", "server.py"]
