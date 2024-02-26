from flask import Flask, request, render_template, redirect, url_for
from time import sleep
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

@app.route('/auth/', methods=['GET', 'POST'])
def auth():
    with open(conf.auth_json, 'r') as json_file:
        auth_url = json.load(json_file)['auth_url']
    if request.method == 'POST':
        auth_token = request.form['auth_token']
        stream_id = request.form['stream_id']
        send_token(auth_token, stream_id)
        sleep(1)
        with open(conf.auth_json, 'r') as json_file:
            data = json.load(json_file)
            if data['authorized'] == True:
                return redirect(url_for('interface'))
            else:
                return render_template('auth.html', auth_url=auth_url, error=True)
    return render_template('auth.html', auth_url=auth_url)

@app.route('/', methods=['GET'])  
def interface():
    with open(conf.auth_json, 'r') as json_file:
        data = json.load(json_file)
        if data['authorized']:
            stream_id = data['stream_id']
            return render_template('interface.html', stream_id=stream_id)
        else:
            return redirect(url_for('auth'))

if __name__ == '__main__':
    app.run(debug=True, port=conf.app_port, host=conf.app_host)
