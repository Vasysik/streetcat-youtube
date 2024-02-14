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
    font_file = "./CALIBRI.TTF"
   
    # Logging settings
    use_logging = False
   
    # Live stream settings
    live_stream_id = ""
   
    # Goggle API Flow settings (only works if use_flow_server == True)
    use_flow_server = False
    flow_server_host = "localhost"
    flow_server_port = 8080
    flow_open_browser = False

    # Client keys
    rtmp_key = ""
    client_id = ""
    client_secret = ""
    ```

## Installation guide (Docker):
