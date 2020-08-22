from pymunk import *
from pygame import *
from Drone import Drone
from Screen import Screen


class Symulation:
    running = True
    space = Space()
    drone = Drone()
    screen = Screen(space)
    clock = time.Clock()
    fps = 35

    def __init__(self):
        self.space.gravity = 0, -980.7
        self.space.damping = 0.3
        self.space.add(self.drone.GetDrone())

    def Start(self):
        while self.running:
            for ev in event.get():
                if key.get_pressed()[K_ESCAPE]:
                    self.running = False
                if ev.type == KEYDOWN:
                    if ev.key == K_UP:
                        self.drone.moveDirection[0] = True
                    if ev.key == K_DOWN:
                        self.drone.moveDirection[1] = True
                    if ev.key == K_RIGHT:
                        self.drone.moveDirection[2] = True
                    if ev.key == K_LEFT:
                        self.drone.moveDirection[3] = True
                if ev.type == KEYUP:
                    if ev.key == K_UP:
                        self.drone.moveDirection[0] = False
                    if ev.key == K_DOWN:
                        self.drone.moveDirection[1] = False
                    if ev.key == K_RIGHT:
                        self.drone.moveDirection[2] = False
                    if ev.key == K_LEFT:
                        self.drone.moveDirection[3] = False
            if mouse.get_pressed()[0]:
                pos = mouse.get_pos()
                if 10 <= pos[0] <= 120:
                    if 250 <= pos[1] <= 270:
                        self.drone.logicModel = "Neural Network"
                        self.fps = 35
                        self.screen.repeats = 2
                    elif 280 <= pos[1] <= 300:
                        self.drone.logicModel = "Fuzzy Logic"
                        self.fps = 60
                        self.screen.repeats = 4
            self.drone.Move()
            self.screen.UpdateScreen(self.space, self.drone)
            self.UpdateTimes()

    def UpdateTimes(self):
        dt = 1. / self.fps
        self.space.step(dt)
        self.clock.tick(self.fps)
