import pymunk
import pygame as pg
from config import FRICTION, ELASTICITY, WIDTH
from data import grades
from events import GAME_OVER


class Bug:
    def __init__(self, pos=None, grade=None, kinematic=False):
        self.grade = grade or grades.get_ramdom_grade()
        self.mass = self.grade.mass
        self.radius = self.grade.radius
        self.color = self.grade.color
        self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        if kinematic:
            self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        else:
            self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = pos or (WIDTH / 2, self.radius)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = ELASTICITY
        self.shape.friction = FRICTION
        self.shape.color = self.color
        self.shape.collision_type = 1
        if kinematic:
            self.shape.collision_type = 4
            return

    def make_dynamic(self):
        self.body.body_type = pymunk.Body.DYNAMIC
        self.body.mass = self.mass
        self.body.moment = self.moment


def get_middle_point(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    return x, y


def collision_callback(arbiter, space, data):
    """Обрабатывает столкновения жуков"""
    items = arbiter.shapes
    if items[0].radius == items[1].radius:
        from data import score

        score.add(items[1].radius)
        pos = get_middle_point(*(item.body.position for item in items))
        space.remove(*items, *(shape.body for shape in items))
        bug = Bug(pos=pos, grade=grades.next_grade(items[0].radius))
        space.add(bug.body, bug.shape)
    return True


def sensor_callback(arbiter, space, data):
    """Обрабатывает столкновение с крышей"""
    pg.event.post(GAME_OVER)
    return True
