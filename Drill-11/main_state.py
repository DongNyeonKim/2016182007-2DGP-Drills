# import random
# import json
# import os
#
# from pico2d import *
# import game_framework
# import game_world
#
# from boy import Boy
# from grass import Grass
# from ball import Ball, BigBall
#
# from brick import Brick
# name = "MainState"
#
# boy = None
# grass = None
# balls = []
# big_balls = []
#
#
# def collide(a, b):
#     left_a, bottom_a, right_a, top_a = a.get_bb()
#     left_b, bottom_b, right_b, top_b = b.get_bb()
#
#     if left_a > right_b: return False
#     if right_a < left_b: return False
#     if top_a < bottom_b: return False
#     if bottom_a > top_b: return False
#
#     return True
#
#
#
#
# def enter():
#     global boy
#     boy = Boy()
#     game_world.add_object(boy, 1)
#
#     global grass
#     grass = Grass()
#     game_world.add_object(grass, 0)
#
#     global balls
#     balls = [Ball() for i in range(10)] + [BigBall() for i in range(10)]
#     game_world.add_objects(balls, 1)
#
#     global brick
#     brick = Brick()
#     game_world.add_object(brick,1)
#     # fill here for balls
#
#
#
#
#
# def exit():
#     game_world.clear()
#
# def pause():
#     pass
#
#
# def resume():
#     pass
#
#
# def handle_events():
#     events = get_events()
#     for event in events:
#         if event.type == SDL_QUIT:
#             game_framework.quit()
#         elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
#                 game_framework.quit()
#         else:
#             boy.handle_event(event)
#
#
# def update():
#     for game_object in game_world.all_objects():
#         game_object.update()
#
#     for ball in balls:
#         if collide(boy, ball):
#             balls.remove(ball)
#             game_world.remove_object(ball)
#             print("COLLISION")
#
#     for ball in balls:
#         if collide(grass, ball):
#             ball.stop()
#         if collide(brick, ball):
#             ball.x = ball.x + brick.velocity
#             #공이 벽돌위에 닿을 경우에만 멈춤
#             if brick.x + 90 >= ball.x >= brick.x - 90:
#                 ball.onthebrick()
#
#     if collide(boy,brick):
#         boy.check =1
#         boy.x = boy.x + brick.velocity
#         if brick.x + 90 > boy.x > brick.x - 90:
#             # # boy.y += 2
#             # boy.y - 50
#             pass
#             #boy.onthebrick()
#
#
#     elif not collide(boy, brick):
#         boy.check =0
#     # fill here for collision check
#
#
#
# def draw():
#     clear_canvas()
#     for game_object in game_world.all_objects():
#         game_object.draw()
#     update_canvas()
#
#
#
#
#
#
import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
from boy import Boy
import main_state

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


animation_names = ['Attack', 'Dead', 'Idle', 'Walk']


class Zombie:
    images = None
    Hp = 0
    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombiefiles/female/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        positions = [(300, 500), (1118, 750), (1050, 530), (575, 220), (235, 33), (575, 220), (1050, 530), (1118, 750)]
        self.patrol_positions = []
        for p in positions:
            self.patrol_positions.append((p[0], 1024 - p[1]))  # convert for origin at bottom, left
        self.patrol_order = 1
        self.target_x, self.target_y = None, None
        self.x, self.y = self.patrol_positions[0]

        self.load_images()
        self.dir = random.random()*2*math.pi # random moving direction
        self.speed = 0
        self.timer = 1.0 # change direction every 1 sec when wandering
        self.frame = 0
        self.build_behavior_tree()
        self.font = load_font('ENCR10B.TTF', 16)

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)
        self.y = clamp(50, self.y, 1024 - 50)

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random() * 2 * math.pi

        return BehaviorTree.SUCCESS

    def find_player(self):
        boy = main_state.get_boy()
        distance = (boy.x - self.x) **2 + (boy.y - self.y)**2
        if distance < (PIXEL_PER_METER * 8) **2:
            self.dir = math.atan2(boy.y - self.y, boy.x - self.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        if Boy.Hp < Zombie.Hp:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def away_from_player(self):
        self.speed = -2 * RUN_SPEED_PPS
        self.calculate_current_position()
        if Boy.Hp < Zombie.Hp:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def get_next_position(self):
        self.target_x, self.target_y = self.patrol_positions[self.patrol_order % len(self.patrol_positions)]
        self.patrol_order += 1
        self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x)
        return BehaviorTree.SUCCESS

    def move_to_target(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()

        distance = (self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2

        if distance < PIXEL_PER_METER ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        #
        away_from_player_node = LeafNode("Away from Player", self.away_from_player)

        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)

        away_node = SequenceNode("Away")
        away_node.add_children(find_player_node, away_from_player_node)

        find_node = SelectorNode("Find")
        find_node.add_children(chase_node, away_node)

        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(find_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.bt.run()

    def draw(self):

        if math.cos(self.dir) < 0:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            else:
                if Zombie.Hp > Boy.Hp:
                    Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
                else:
                    Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)
        else:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].draw(self.x, self.y, 100, 100)
            else:
                if Zombie.Hp > Boy.Hp:
                    Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)
                else:
                    Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)

        self.font.draw(self.x - 60, self.y + 50, '(%.0d)' % Zombie.Hp, (255, 255, 0))

    def handle_event(self, event):
        pass
