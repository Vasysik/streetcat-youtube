from google_auth_oauthlib.flow import Flow
from time import sleep
import conf
import json

def Authorize(file):
    flow = Flow.from_client_secrets_file(file, scopes=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://www.googleapis.com/auth/youtube.readonly',
        ],
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    if conf.web_auth: return flow_server(flow)
    return flow_local(flow)

def flow_server(flow):
    auth_data = {"auth_url": flow.authorization_url()[0],
                 "auth_token": "",
                 "stream_id": "",
                 "authorized": False}
    with open(conf.auth_json, 'w') as auth_json:
        json.dump(auth_data, auth_json)

    token = ""
    stream_id = ""
    while token == "" or stream_id == "":
        try:
            with open(conf.auth_json, 'r') as auth_json:
                data = json.loads(auth_json.read())
                token = data["auth_token"]
                stream_id = data["stream_id"]
        except: None
        sleep(0.1)
    
    try: 
        flow.fetch_token(code=token)
        with open(conf.auth_json, 'w') as auth_json:
            auth_data["auth_url"] = ""
            auth_data["authorized"] = True
            json.dump(auth_data, auth_json) 
        return [flow, stream_id]
    except: return flow_server(flow)

def flow_local(flow):
    print(f"Please visit this URL to authorize this application: {flow.authorization_url()[0]}")
    flow.fetch_token(code=input("Enter the authorization code: "))
    return [flow, ""]