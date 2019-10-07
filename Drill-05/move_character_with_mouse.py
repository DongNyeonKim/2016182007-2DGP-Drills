from pico2d import *


KPU_WIDTH, KPU_HEIGHT = 1280, 1024


def handle_events():
    global running
    global mouse_x, mouse_y
    global direct
    global mouse_click_x, mouse_click_y
    global character_x, character_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouse_click_x, mouse_click_y = event.x - 20, KPU_HEIGHT - 1 - event.y + 25
            if mouse_click_x < character_x:
                direct = 0
            elif character_x < mouse_click_x:
                direct = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


open_canvas(KPU_WIDTH, KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('hand_arrow.png')
character_man = load_image('animation_sheet.png')

running = True
mouse_x, mouse_y = KPU_WIDTH // 2, KPU_HEIGHT // 2
mouse_click_x, mouse_click_y = 600, 550
character_x, character_y = 600, 550
frame = 0
direct = 1
i = 1
hide_cursor()

while running:
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character_man.clip_draw(frame * 100, (99 * direct) + 1, 100, 100, character_x, character_y)
    character.clip_draw(0, 0, 50, 50, mouse_x, mouse_y)
    if i < 100:
        i = 1
        t = i / 100
        character_x = (1 - t) * character_x + t * mouse_click_x
        character_y = (1 - t) * character_y + t * mouse_click_y
    i += 1
    update_canvas()
    frame = (frame + 1) % 8

    handle_events()

close_canvas()
