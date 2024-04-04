FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir awscli boto3

COPY Deploy.py /app/Deploy.py

CMD ["python", "Deploy.py"]
