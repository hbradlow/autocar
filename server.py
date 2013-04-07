from flask import Flask
from controller import get_blobs
import thread

lock = thread.allocate_lock()

b = "this"

app = Flask(__name__)

def update(s):
    global b
    while True:
        tmp = get_blobs()
        if tmp:
            with lock:
                b = tmp

@app.route("/")
def hello():
    global b
    with lock:
        if b:
            s = str(b[0]) + "," + str(b[1])
            return s
        return ""

if __name__ == "__main__":
    thread.start_new_thread(update,("a",))
    app.run(host="10.22.34.6",port=8080)
