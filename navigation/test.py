import Tkinter as tk
import numpy as np
from gui import Visualizer, Point2D
from env import Env

e = Env()

def key_callback(event):
    e.move()
    e.draw(vis)
    vis.draw()

root = tk.Tk()
vis = Visualizer(root,800,600,key_callback=key_callback)

e.draw(vis)

vis.run()
root.mainloop()
