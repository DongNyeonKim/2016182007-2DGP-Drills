from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

x=0
frame = 0
while True :
    while (x< 800):
        clear_canvas()
        grass.draw(400,30)
        character.clip_draw(frame * 100, 100, 100, 100, x, 90)
        update_canvas()
        frame = (frame+1)%8
        x += 1
    while (x > 10):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(frame * 100, 0, 100, 100, x, 90)
        update_canvas()
        frame = (frame - 1) % 8
        x -= 1

    delay(0.02)
    get_events()
    

close_canvas()

