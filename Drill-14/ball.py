from pico2d import *
import game_world
import game_framework
import background
import random

class Ball:
    image =None

    def __init__(self):
        if Ball.image == None:
            Ball.image = load_image('ball41x41.png')

        self.x = 0
        self.y = 0
        self.cx, self.cy = 0,0

        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()

    def get_bb(self):
        return self.cx -20, self.cy -20, self.cx +20, self.cy +20

    def draw(self):
        self.cx = self.x - self.bg.window_left
        self.cy = self.y - self.bg.window_bottom
        self.image.draw(self.cx, self.cy)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def set_background(self, bg):
        self.bg = bg
        self.x = random.randint(50,1800-50)
        self.y = random.randint(50, 1100-50)