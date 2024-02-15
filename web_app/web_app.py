from flask import Flask, request, render_template
import json
import conf 

app = Flask(__name__)

def send_token(auth_token, stream_id):
    with open(conf.auth_json, 'r') as json_file:
        data = json.load(json_file)
        data['auth_token'] = auth_token
        data['stream_id'] = stream_id
    with open(conf.auth_json, 'w') as json_file:
        json.dump(data, json_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        auth_token = request.form['auth_token']
        stream_id = request.form['stream_id']
        send_token(auth_token, stream_id)
        return render_template('success.html', auth_token=auth_token, stream_id=stream_id)
    with open(conf.auth_json, 'r') as json_file:
        auth_url = json.load(json_file)['auth_url']
    return render_template('index.html', auth_url=auth_url)

if __name__ == '__main__':
    app.run(debug=True, port=conf.app_port, host=conf.app_host)