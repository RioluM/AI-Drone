from pygame import *
from pymunk import pygame_util
from pymunk import *


class Screen:
    textSurface = [0, 0, 0, 0, 0, 0]

    def __init__(self, space):
        init()
        font.init()
        self.font = font.SysFont('Comic Sans MS', 24)
        self.font2 = font.SysFont('arial', 14)
        self.screen = display.set_mode(flags=FULLSCREEN)
        self.draw_options = pygame_util.DrawOptions(self.screen)
        self.StaticObjects(space)
        self.updateCounter = 0
        self.button1 = self.font2.render("Neural Network", False, (0, 0, 0))
        self.button2 = self.font2.render("Fuzzy Logic", False, (0, 0, 0))
        self.repeats = 2

    def StaticObjects(self, space):
        ground = Segment(space.static_body, (0, 20), (self.screen.get_width(), 20), 20)
        ground.color = (102, 51, 0, 255)
        space.add(ground)

    def UpdateScreen(self, space, drone):
        self.screen.fill(Color(0, 102, 153))
        info1, info2, info3, info4, info5, info6 = drone.GetStringInfo()
        if self.updateCounter == 0:
            self.textSurface[0] = self.font.render(info1, False, (0, 0, 0))
            self.textSurface[1] = self.font.render(info2, False, (0, 0, 0))
            self.textSurface[2] = self.font.render(info3, False, (0, 0, 0))
            self.textSurface[3] = self.font.render(info4, False, (0, 0, 0))
            self.textSurface[4] = self.font.render(info5, False, (0, 0, 0))
        self.textSurface[5] = self.font.render(info6, False, (0, 0, 0))
        self.screen.blit(self.textSurface[0], (0, 0))
        self.screen.blit(self.textSurface[1], (0, 50))
        self.screen.blit(self.textSurface[2], (0, 100))
        self.screen.blit(self.textSurface[3], (0, 150))
        self.screen.blit(self.textSurface[4], (0, 200))
        self.screen.blit(self.textSurface[5], (self.screen.get_width()/2-100, 0))
        self.updateCounter = (self.updateCounter+1) % self.repeats
        draw.rect(self.screen, Color(255,255,255), (10, 250, 110, 20))
        self.screen.blit(self.button1, (15, 250))
        draw.rect(self.screen, Color(255,255,255), (10, 280, 110, 20))
        self.screen.blit(self.button2, (25, 280))
        space.debug_draw(self.draw_options)
        display.update()
