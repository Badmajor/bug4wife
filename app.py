import pygame as pg
import pymunk.pygame_util
from pymunk import Vec2d

from data import grades
from objects import collision_callback, create_bug, preview_bug

pymunk.pygame_util.positive_y_is_up = False

#Настройки PyGame
RES = WIDTH, HEIGHT = 600, 1300
FPS = 120

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

# Переменные Pymunk
space = pymunk.Space()
space.gravity = 0, 6000
# Стены и пол
segment_floor = pymunk.Segment(space.static_body, (1, HEIGHT), (WIDTH, HEIGHT), 50)
left_wall = pymunk.Segment(space.static_body, (0, 0), (1, HEIGHT), 25)
right_wall = pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH - 1, HEIGHT), 25)
space.add(segment_floor, left_wall, right_wall)
segment_floor.friction = 1

# Обработка столкновений
collision_handler = space.add_default_collision_handler()
collision_handler.begin = collision_callback

#Превью жука
grade = grades.get_ramdom_grade()
pr_bug = preview_bug(space, grade)


#Отрисовка PyGame
while True:
    surface.fill(pg.Color('white'))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEMOTION:
            pr_bug.body.position = (event.pos[0], 0)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                space.remove(pr_bug)
                create_bug(space, event.pos, grade)
                grade = grades.get_ramdom_grade()
                pr_bug = preview_bug(space, grade)

    space.step(1 / FPS)
    space.debug_draw(draw_options)

    pg.display.flip()
    clock.tick(FPS)
