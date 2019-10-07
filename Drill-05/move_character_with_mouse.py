from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024


def handle_events():
    global running
    global x, y
    global mx, my
    global tempx, tempy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            x,y = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            mx,my = event.x-20, KPU_HEIGHT - 1 - event.y+30
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def draw_line(p1, p2):
    a = 0
    for i in range(0, 100 + 1, 2):
        t = i / 100
        x = (1 - t) * p1[0] + t * p2[0]
        y = (1 - t) * p1[1] + t * p2[1]
        if x < a:
            character_man.clip_draw(frame*100, 1 * 1, 100, 100, x, y)
        else:
            character_man.clip_draw(frame*100, 100 * 1, 100, 100, x, y)
    a=x

def draw_line_L(p1, p2):
    for i in range(0, 100 + 1, 2):
        t = i / 100
        x = (1 - t) * p1[0] + t * p2[0]
        y = (1 - t) * p1[1] + t * p2[1]
        character_man.clip_draw(100, 100 * 1, 100, 100, x, y)
        #character_man.clip_draw(frame*100, 1 * 1, 100, 100, x, y)

open_canvas(KPU_WIDTH,KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('hand_arrow.png')
character_man = load_image('animation_sheet.png')

running = True
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
mx, my = x, y
tempx, tempy=x, y
frame = 0
hide_cursor()

while running:
    clear_canvas()
    a=1
    if a==1:
        character_man.clip_draw(frame * 100, 100 * 1, 100, 100, mx, my)
        a=0
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    draw_line((tempx, tempy),(mx,my))
    tempx, tempy = mx, my
#    character_man.clip_draw(frame * 100, 100 * 1, 100, 100, mx, my)
    character.clip_draw(0, 0, 50, 50, x, y)
    update_canvas()
    frame = (frame + 1) % 8

    handle_events()

close_canvas()




