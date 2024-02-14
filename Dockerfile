FROM python:3.10
ADD streetcat_youtube.py .
ADD auth_youtube.py .
ADD CALIBRI.TTF .
ADD requirements.txt .
RUN apt update
RUN apt install ffmpeg -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "-u", "streetcat_youtube.py" ]