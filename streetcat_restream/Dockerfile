FROM python:3.10
ADD streetcat_youtube.py .
ADD auth_youtube.py .
ADD CALIBRI.TTF .
ADD requirements.txt .
RUN apt update && \
    apt install ffmpeg -y && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt