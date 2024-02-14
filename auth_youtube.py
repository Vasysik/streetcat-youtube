from google_auth_oauthlib.flow import InstalledAppFlow
# from google_auth_oauthlib.flow import Flow
import conf

client_id = conf.client_id
client_secret = conf.client_secret

def Authorize(file):
    flow = InstalledAppFlow.from_client_secrets_file(file, scopes={
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://www.googleapis.com/auth/youtube.readonly',
    })
    if conf.use_flow_server:
        flow.run_local_server(host=conf.flow_server_host, 
                            port=conf.flow_server_port, 
                            authorization_prompt_message='Please visit this URL to authorize this application: {url}', 
                            success_message='The authentication flow has completed. You may close this window.', 
                            open_browser=conf.flow_open_browser)
    else: flow.run_console()    

    # flow = Flow.from_client_secrets_file(file, scopes=[
    #     'openid',
    #     'https://www.googleapis.com/auth/userinfo.email',
    #     'https://www.googleapis.com/auth/userinfo.profile',
    #     'https://www.googleapis.com/auth/youtube',
    #     'https://www.googleapis.com/auth/youtube.force-ssl',
    #     'https://www.googleapis.com/auth/youtube.readonly',
    #     ],
    #     redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    # with open("auth_link.txt", "w") as auth_file:
    #     auth_file.write(flow.authorization_url()[0])

    # flow.fetch_token(code=input())

    return flow
