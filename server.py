from flask import Flask
from flask import request
from controller import get_blobs
import json
import thread

lock = thread.allocate_lock()

b = "this"

app = Flask(__name__)

def update(s):
    global b
    while True:
        tmp = get_blobs()
        for index,l in enumerate(tmp):
            l.append(index)
        if tmp:
            with lock:
                b = tmp

@app.route("/make_point")
def make_point():
    x = request.args.get('x')
    y = request.args.get('y')
    print x,y
    return "worked"

@app.route("/")
def hello():
    global b
    with lock:
        if b:
            s = json.dumps(b)
            return s
        return ""

if __name__ == "__main__":
    thread.start_new_thread(update,("a",))
    app.run(host="10.22.34.218",port=8080)
