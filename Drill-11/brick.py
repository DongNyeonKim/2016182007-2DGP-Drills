from pico2d import *
import game_world
import game_framework

MIN_FALL_SPEED = 50
MAX_FALL_SPEED = 200

class Brick:
    image = None
    x = 200
    y = 200
    def __init__(self):
        if Brick.image == None:
            Brick.image = load_image('brick180x40.png')
        #self.x = 200
        #self.y = 200
        self.speed = 300
        self.dir=0
        self.velocity=0

    def get_bb(self):
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
        # fill here for draw

    def update(self):
        #브릭의 이동
        if self.x <= 0+90:
            self.dir = 0
        if self.x >= 1600-90:
            self.dir = 1
        if self.dir==0:
            self.velocity = self.speed * game_framework.frame_time
            self.x += self.velocity
        elif self.dir==1:
            self.velocity = -(self.speed * game_framework.frame_time)
            self.x += self.velocity

        # self.x += self.velocity
