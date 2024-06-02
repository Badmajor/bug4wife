import pygame as pg
import pymunk.pygame_util

from config import CREATION_DELAY, WIDTH, HEIGHT, FPS, ELASTICITY, DEBUG
from data import score
from events import GAME_OVER_TYPE
from objects import collision_callback, sensor_callback, Bug

pymunk.pygame_util.positive_y_is_up = False

# Настройки PyGame
RES = WIDTH, HEIGHT


pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

# Переменные Pymunk
space = pymunk.Space()
space.gravity = 0, 6000
font = pg.font.Font(None, 35)

# Стены и пол
floor = pymunk.Segment(space.static_body, (1, HEIGHT), (WIDTH, HEIGHT), 50)
left_wall = pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 25)
right_wall = pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 25)
roof = pymunk.Segment(space.static_body, (0, -10), (WIDTH, -10), 1)
roof.sensor = True
roof.collision_type = 3
space.add(floor, left_wall, right_wall, roof)
floor.friction = 1
floor.elasticity = ELASTICITY

# Обработка столкновений
collision_handler = space.add_collision_handler(1, 1)
collision_handler.post_solve = collision_callback

roof_touch_handler = space.add_collision_handler(1, 3)
roof_touch_handler.pre_solve = sensor_callback

roof_touch_handler = space.add_collision_handler(1, 4)
roof_touch_handler.begin = lambda *args, **kwargs: True


# Превью жука
bug = Bug(kinematic=True)
space.add(bug.body, bug.shape)

last_bug_creation_time = 0

game = True
# Отрисовка PyGame
while game:
    surface.fill(pg.Color("white"))
    current_time = pg.time.get_ticks()
    if (
        bug.shape.collision_type == 1
        and current_time - last_bug_creation_time > CREATION_DELAY
    ):
        bug = Bug(kinematic=True)
        space.add(bug.body, bug.shape)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEMOTION:
            if bug.shape.collision_type != 1:
                bug.body.position = (event.pos[0], bug.radius)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if bug.shape.collision_type != 1:
                    score.add(1)
                bug.make_dynamic()
                bug.shape.collision_type = 1
                last_bug_creation_time = current_time
        if event.type == GAME_OVER_TYPE:
            game = False

    space.step(1 / FPS)
    if DEBUG:
        space.debug_draw(draw_options)

    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            angle_degrees = (
                -shape.body.angle * 57.2958
            )  # преобразование радианов в градусы
            position = shape.body.position
            radius = shape.radius
            if "bug_image" not in shape.__dict__:
                bug_image = pg.image.load("favicon.png")
                shape.bug_image = pg.transform.scale(
                    bug_image, (radius * 2 + 2, radius * 2 + 2)
                )
            bug_image_with_bg = pg.Surface(shape.bug_image.get_size(), pg.SRCALPHA)
            pg.draw.circle(bug_image_with_bg, shape.color, (radius, radius), radius)
            bug_image_with_bg.blit(shape.bug_image, (0, 0))
            rotated_img = pg.transform.rotate(bug_image_with_bg, angle_degrees)
            rotated_rect = rotated_img.get_rect(center=(position.x, position.y))
            surface.blit(rotated_img, rotated_rect.topleft)

    score_table = font.render(f"{score}", True, pg.Color("red"))
    surface.blit(score_table, (25, HEIGHT - 40))

    pg.display.flip()
    clock.tick(FPS)
else:
    font = pg.font.Font(None, 74)
    game_over = font.render("Game Over ", True, pg.Color("red"))
    score_table = font.render(f"{score}", True, pg.Color("red"))
    surface.blit(game_over, (200, 250))
    surface.blit(score_table, (200, 350))
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
