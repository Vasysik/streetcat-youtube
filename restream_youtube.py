import cam_viewer
import pytchat
import conf
import _thread
import time
from googleapiclient.discovery import build
from auth_youtube import Authorize
import logging
import json

with open('cams.json', 'r') as file:
    cams_json = json.loads(file.read())

logging.basicConfig(filename=f"viewer.log", level=logging.INFO)
httpx_logger = logging.getLogger("httpx")
httpx_logger.disabled = True

authResponse = Authorize('client.json')
credentials = authResponse.credentials
youtube = build('youtube', 'v3', credentials=credentials)

command = "ffmpeg -re -i"
parameters = "-pix_fmt yuvj420p -x264-params keyint=48:min-keyint=48:scenecut=-1 -b:v 4500K -b:a 128k -minrate 4000k -maxrate 4500k -bufsize 1835k -bf 2 -coder 1 -profile:v high -ar 44100 -acodec aac -vcodec libx264 -preset slow -crf 28 -threads 4 -cpu-used 0 -r 30 -f flv rtmp://a.rtmp.youtube.com/live2/" + conf.rtmp_key

def getLiveChatId(LIVE_STREAM_ID):
    stream = youtube.videos().list(
        part="liveStreamingDetails",
        id=LIVE_STREAM_ID,
    )
    response = stream.execute()
    liveChatId = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
    print(f"LiveChatID: {liveChatId}")
    logging.info(f"{cam_viewer.current_time()} | LiveChatID: {liveChatId}")
    return liveChatId

stream_id = input("Enter the live stream ID: ")
chat = pytchat.create(video_id = stream_id)
liveChatId = getLiveChatId(stream_id)

def sendReplyToLiveChat(liveChatId, message):
    reply = youtube.liveChatMessages().insert(
        part="snippet",
        body={
            "snippet": {
                "liveChatId": liveChatId,
                "type": "textMessageEvent",
                "textMessageDetails": {
                    "messageText": message,
                }
            }
        }
    )
    response = reply.execute()

def checker():
    while True:
        if cam_viewer.cam_proc is None or cam_viewer.cam_proc.poll() is not None:
            sendReplyToLiveChat(liveChatId, "Cams Rebooting...")
            player = cam_viewer.playback(command = command, 
                                parameters = parameters,
                                cam_name = "fresh",
                                cams_json = cams_json,
                                use_text = True,
                                fontfile = conf.fontfile)
            sendReplyToLiveChat(liveChatId, player[1])
        cam_viewer.cam_proc.wait()

_thread.start_new_thread(checker, ())

logging.info(f"{cam_viewer.current_time()} | Chat listener launch...")
while chat.is_alive():
    try:
        for c in chat.get().sync_items():
            print(f"Chat | {c.author.name}: {c.message}")
            logging.info(f"{cam_viewer.current_time()} | Chat | {c.author.name}: {c.message}")
            if c.message.split()[0] == "!cam" and len(c.message.split()) == 3:
                com, cam_name, cam_number = c.message.split()
                player = cam_viewer.playback(command = command, 
                                    parameters = parameters, 
                                    cams_json = cams_json,
                                    cam_name = cam_name, 
                                    cam_number = cam_number,
                                    use_text = True,
                                    fontfile = conf.fontfile)
                sendReplyToLiveChat(liveChatId, player[1])
            elif c.message.split()[0] == "!rand":
                player = cam_viewer.playback(command = command, 
                                    parameters = parameters,
                                    cams_json = cams_json,
                                    use_text = True,
                                    fontfile = conf.fontfile)
                sendReplyToLiveChat(liveChatId, player[1])
    except:
        logging.error(f"{cam_viewer.current_time()} | Chat | ERROR") 
        print("Chat | ERROR")
logging.error(f"{cam_viewer.current_time()} | Chat is not alive!!!")
