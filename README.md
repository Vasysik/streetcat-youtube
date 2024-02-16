# StreetCat-youtube

## Installation guide:
1) Install [git](https://git-scm.com/downloads)
2) Install [docker](https://docs.docker.com/engine/install/)
3) Download the streetcat-youtube repository:
   ```
   git clone https://github.com/Vasysik/streetcat-youtube/
   cd .\streetcat-youtube\
   git submodule update --init
   ```
4) Create a ```conf.py``` file containing:
   ```
   # Goggle API Flow settings
   auth_json = "auth.json"
   web_auth = True
   
   # Web App settings
   app_host = "0.0.0.0"
   app_port = 8080
   
   # Client keys for streaming
   rtmp_key = ""
   client_json = "client.json"
   
   # FFMPEG settings
   command = "ffmpeg -fflags +igndts -fflags +discardcorrupt -re -i"
   parameters = f"-pix_fmt yuvj420p -x264-params keyint=48:min-keyint=48:scenecut=-1 -b:v 4500K -b:a 128k -minrate 4000k \
               -maxrate 4500k -bufsize 1835k -bf 2 -coder 1 -profile:v high -ar 44100 -acodec aac -vcodec libx264 -preset slow -crf 28 \
               -threads 4 -cpu-used 0 -r 30 -f flv rtmp://a.rtmp.youtube.com/live2/{rtmp_key}"
   use_text = True
   font_file = "./CALIBRI.TTF"
   
   # Logging settings
   use_logging = False
   ```
5) 
