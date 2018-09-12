from flask import Flask
import os
import socket

app = Flask(__name__)

def hostname():
    var_check = os.environ.get('REPLY_HOSTNAME')
    if var_check:
        return var_check
    if var_check == 'unset':
        return socket.gethostname()
    else:
        return socket.gethostname()

@app.route('/')
def hello():
    host_name = hostname()
    return "Hello, I'm %s" % host_name

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 11000)
