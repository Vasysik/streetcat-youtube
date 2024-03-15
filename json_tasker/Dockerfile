FROM python:3.10
ADD tasker.py .
ADD requirements.txt .
RUN apt update && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt