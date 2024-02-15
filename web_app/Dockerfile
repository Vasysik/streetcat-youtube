FROM python:3.10
ADD web_app.py .
ADD requirements.txt .
COPY templates ./templates
COPY static ./static
RUN apt update && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt