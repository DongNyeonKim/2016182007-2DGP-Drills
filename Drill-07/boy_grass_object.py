from pico2d import *
import random
# Game object class here
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400,30)

class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100,700),90
        self.frame = 0
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = random.randint(0, 7)
        self.x +=5

    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)



def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# initialization code
open_canvas()

ballcount=  random.randint(5,15)

grass = Grass()
team =[Boy() for i in range(11)]
SmallBall_team = [SmallBall() for i in range(ballcount)]
BigBall_team = [BigBall() for i in range(20-ballcount)]

running = True

# game main loop code
while running:
    handle_events()

    for boy in team:
        boy.update()
    for SmallBall in SmallBall_team:
        SmallBall.update()
    for BigBall in BigBall_team:
        BigBall.update()
    clear_canvas()
    grass.draw()

    for boy in team:
        boy.draw()
    for SmallBall in SmallBall_team:
        SmallBall.draw()
    for BigBall in BigBall_team:
        BigBall.draw()
    update_canvas()

    delay(0.05)

# finalization code
close_canvas()