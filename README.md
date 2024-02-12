# StreetCat-youtube

## Installation guide (Local):
1) Install [Python 3.10](https://www.python.org/downloads/)
2) Install [git](https://git-scm.com/downloads)
3) Install [ffmpeg](https://ffmpeg.org/download.html)
4) Download the streetcat-youtube repository:
   ```
   git clone https://github.com/Vasysik/streetcat-youtube/
   cd .\streetcat-youtube\
   ```
5) Install all remaining required libraries:
   ```
   pip install -r requirements.txt
   ```
6) Create a ```conf.py``` file containing:
    ```
    # Font file location for text in FFMEG
    fontfile = "./CALIBRI.TTF"

    # Client keys for restream_youtube.py
    rtmp_key = ""
    client_id = ""
    client_secret = ""
    ```

## Installation guide (Docker):
