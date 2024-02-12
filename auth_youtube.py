from google_auth_oauthlib.flow import InstalledAppFlow
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
    flow.run_console()
    return flow
