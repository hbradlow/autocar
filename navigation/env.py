import numpy as np
import math
from gui import Point2D, Line2D
import random

class State:
    def __init__(self,position,angle):
        self.position = position
        self.angle = angle
    def draw(self,vis):
        vis.add_drawable(Point2D(self.position))
    def distance_to(self,goal):
        return np.linalg.norm(self.position-goal)
    def __repr__(self):
        return str(self.position)
class Car:
    def __init__(self,start_state=State(np.array([0,0]),0)):
        self.current_state = start_state
    def get_children(self,num_states=5,field_of_view=.2,distance=30):
        def state_at(distance, angle):
            a = angle + self.current_state.angle
            x = math.cos(a)*distance
            y = math.sin(a)*distance
            s = State(self.current_state.position+np.array([x,y]),a)
            return s
        half = num_states/2.
        states = []
        for i in range(num_states):
            angle = (i-half)*field_of_view
            s = state_at(distance,angle)
            states.append(s)
        return states
    def draw(self,vis):
        self.current_state.draw(vis)

class Env:
    def __init__(self,goal=np.array([300,300])):
        self.goal = goal
        self.car = Car(start_state=State(np.array([100,100]),0))
    def move(self):
        self.move_greedy()
    def move_greedy(self):
        next = min(self.car.get_children(),key=lambda s: s.distance_to(self.goal))
        self.car.current_state = next
    def draw(self,vis):
        self.car.draw(vis)
        vis.add_drawable(Point2D(self.goal,radius=20,fill="green"))
        for state in self.car.get_children():
            vis.add_drawable(Line2D(self.car.current_state.position,state.position))
            state.draw(vis)
