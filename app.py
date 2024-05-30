import pygame as pg
import pymunk.pygame_util

from config import CREATION_DELAY
from data import grades, score
from events import GAME_OVER, GAME_OVER_TYPE
from objects import collision_callback, create_bug, preview_bug, sensor_callback

pymunk.pygame_util.positive_y_is_up = False

# Настройки PyGame
RES = WIDTH, HEIGHT = 600, 1000
FPS = 120

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

# Переменные Pymunk
space = pymunk.Space()
space.gravity = 0, 6000

# Стены и пол
floor = pymunk.Segment(space.static_body, (1, HEIGHT), (WIDTH, HEIGHT), 50)
left_wall = pymunk.Segment(space.static_body, (0, 0), (1, HEIGHT), 25)
right_wall = pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH - 1, HEIGHT), 25)
roof = pymunk.Segment(space.static_body, (0, -10), (WIDTH, -10), 1)
roof.sensor = True
roof.collision_type = 3
space.add(floor, left_wall, right_wall, roof)
floor.friction = 1

# Обработка столкновений
collision_handler = space.add_collision_handler(1, 1)
collision_handler.pre_solve = collision_callback

roof_touch_handler = space.add_collision_handler(1, 3)
roof_touch_handler.pre_solve = sensor_callback
# Превью жука
grade = grades.get_ramdom_grade()
pr_bug = preview_bug(space, grade)

last_bug_creation_time = 0

game = True
# Отрисовка PyGame
while game:
    surface.fill(pg.Color('white'))
    current_time = pg.time.get_ticks()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEMOTION:
            pr_bug.body.position = (event.pos[0], 0)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and current_time - last_bug_creation_time > CREATION_DELAY:
                score.add(1)
                space.remove(pr_bug)
                create_bug(space, event.pos, grade)
                grade = grades.get_ramdom_grade()
                pr_bug = preview_bug(space, grade)
                last_bug_creation_time = current_time
        if event.type == GAME_OVER_TYPE:
            game = False

    space.step(1 / FPS)
    space.debug_draw(draw_options)

    pg.display.flip()
    clock.tick(FPS)
else:
    font = pg.font.Font(None, 74)
    text = font.render(f"Game Over "
                       f"{score}", True, pg.Color('red'))
    surface.blit(text, (200, 250))
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

