FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:app"]