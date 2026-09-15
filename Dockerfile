FROM python:3.14-slim

WORKDIR /app

RUN mkdir -p /app/data /app/logs

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY config ./config
COPY start.sh .

CMD ["./start.sh"]

HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
