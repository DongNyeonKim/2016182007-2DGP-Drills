import game_framework
import main_state
from pico2d import *


name = "Pausestate"
image = None
stop = 0

def enter():
    global image
    image = load_image('pause.png')

def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_state()
            #game_framework.change_state(main_state)



def draw():
    clear_canvas()
    a = stop % 200
    if  100>a>0:
        image.clip_draw(200, 200, 500, 500, 400, 300, 200, 200)
    main_state.boy.draw()
    main_state.grass.draw()
    update_canvas()





def update():
    global stop
    stop += 1


def pause():
    pass


def resume():
    pass






