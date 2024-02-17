import cam_viewer
import pytchat
import conf
import _thread
from googleapiclient.discovery import build
from auth_youtube import Authorize
import logging
import json
import time

with open('cams.json', 'r') as file:
    cams_json = json.loads(file.read())

if conf.use_logging:
    logging.basicConfig(filename=f"viewer.log", level=logging.INFO)
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.disabled = True

authResponse = Authorize(conf.client_json)
credentials = authResponse[0].credentials
youtube = build('youtube', 'v3', credentials=credentials)

cam_proc = None

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

stream_id = authResponse[1]
if stream_id == "": stream_id = input("Enter the live stream ID: ")
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

def liveChatListener():
    global cam_proc
    try:
        logging.info(f"{cam_viewer.current_time()} | Chat listener launch...")
        chat = pytchat.create(video_id = stream_id)
        while chat.is_alive():
            try:
                for c in chat.get().sync_items():
                    print(f"Chat | {c.author.name}: {c.message}")
                    logging.info(f"{cam_viewer.current_time()} | Chat | {c.author.name}: {c.message}")
                    if c.message.split()[0] == "!cam" and len(c.message.split()) == 3:
                        com, cam_name, cam_number = c.message.split()
                        player = cam_viewer.playback(command = conf.command, 
                                            parameters = conf.parameters, 
                                            cams_json = cams_json,
                                            cam_name = cam_name, 
                                            cam_number = int(cam_number),
                                            use_text = conf.use_text,
                                            font_file = conf.font_file)
                        cam_proc = player[0]
                        sendReplyToLiveChat(liveChatId, player[1])
                    elif c.message.split()[0] == "!rand":
                        player = cam_viewer.playback(command = conf.command, 
                                            parameters = conf.parameters,
                                            cams_json = cams_json,
                                            use_text = conf.use_text,
                                            font_file = conf.font_file)
                        cam_proc = player[0]
                        sendReplyToLiveChat(liveChatId, player[1])
            except:
                logging.error(f"{cam_viewer.current_time()} | Chat listener error") 
                print("Chat listener error")
    except:
        logging.warning(f"{cam_viewer.current_time()} | Chat is not live! Attempting to reboot...")
        time.sleep(10)
        liveChatListener()

def checker():
    global cam_proc
    while True:
        try:
            if cam_proc is None or cam_proc.poll() is not None:
                sendReplyToLiveChat(liveChatId, "Cams Rebooting...")
                player = cam_viewer.playback(command = conf.command, 
                                    parameters = conf.parameters,
                                    cams_json = cams_json,
                                    use_text = conf.use_text,
                                    font_file = conf.font_file)
                cam_proc = player[0]
                sendReplyToLiveChat(liveChatId, player[1])
            cam_proc.wait()
        except: sendReplyToLiveChat(liveChatId, "Cams Rebooting Error")

_thread.start_new_thread(checker, ())
liveChatListener()