from flask import Flask
from flask import request
from controller import get_blobs, run
import json
import thread
import numpy as np

import IPython

lock = thread.allocate_lock()

b = "this"

app = Flask(__name__)

def update(s):
    global b
    while True:
        tmp = get_blobs()
        print tmp
        if tmp:
            """
            for index,l in enumerate(tmp):
                l.append(index)
            """
            with lock:
                b = tmp
                #print b

@app.route("/make_point")
def make_point():
    global b
    x = float(request.args.get('x'))
    y = float(request.args.get('y'))
    with lock:
        min = 99999999999
        min_blob = None
        print b
        for blob in b:
            n = np.linalg.norm(np.array([x-blob[0],y-blob[1]]))
            if n<min:
                min_blob = blob
                min = n
        print min_blob
        min_x = min_blob[0]*min_blob[2]
        l = [blob[0] for blob in b]
        sum = 0
        for blob in b:
            sum += blob[0]*blob[2]
        ave_x = sum/len(b)

        if min_x<ave_x:
            print "LEFT"
            run(left=True)
        else:
            print "RIGHT"
            run(left=False)
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
