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
    # Logging settings
    use_logging = False
   
    # Live stream settings
    live_stream_id = ""

    # Goggle API Flow settings
    auth_json = "auth.json"
    use_flow_server = True
    flow_server_host = "localhost"
    flow_server_port = 8080
   flow_open_browser = False

    # Client keys for streaming
    rtmp_key = ""
    client_json = ""

    # FFMPEG settings
    command = "ffmpeg -fflags +discardcorrupt -re -i"
    parameters = f"-pix_fmt yuvj420p -x264-params keyint=48:min-keyint=48:scenecut=-1 -b:v 4500K -b:a 128k -minrate 4000k \
                -maxrate 4500k -bufsize 1835k -bf 2 -coder 1 -profile:v high -ar 44100 -acodec aac -vcodec libx264 -preset slow -crf 28 \
                -threads 4 -cpu-used 0 -r 30 -f flv rtmp://a.rtmp.youtube.com/live2/{rtmp_key}"
    use_text = True
    font_file = "./CALIBRI.TTF"
    ```

## Installation guide (Docker):
