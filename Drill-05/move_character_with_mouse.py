from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024


def handle_events():
    global running
    global x , y
    global mx, my
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            x,y = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False



open_canvas(KPU_WIDTH,KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('hand_arrow.png')
character_man = load_image('animation_sheet.png')

running = True
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
mx, my = 100, 100
frame = 0
hide_cursor()

while running:
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character_man.clip_draw(frame * 100, 100 * 1, 100, 100, mx, my)
    character.clip_draw(0, 0, 50, 50, x, y)
    update_canvas()
    frame = (frame + 1) % 8

    handle_events()

close_canvas()




