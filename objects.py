import pymunk

from config import FRICTION, ELASTICITY
from data import grades, Grade


def create_bug(space, pos, grade=None, is_new=True):
    if not grade:
        grade: Grade = grades.get_ramdom_grade()
    mass = grade.mass
    radius = grade.radius
    color = grade.color
    bug_moment = pymunk.moment_for_circle(mass, 0, radius, )
    bug_body = pymunk.Body(mass, bug_moment)
    if is_new:
        bug_body.position = (pos[0], 1)
    else:
        bug_body.position = pos
    bug_shape = pymunk.Circle(bug_body, radius)
    bug_shape.elasticity = ELASTICITY
    bug_shape.friction = FRICTION
    bug_shape.color = color
    space.add(bug_body, bug_shape)


def preview_bug(space, grade):
    radius = grade.radius
    color = grade.color
    bug_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    bug_body.position = (300, 0)
    preview_bug_shape = pymunk.Circle(bug_body, radius)
    preview_bug_shape.color = color
    space.add(bug_body, preview_bug_shape)
    return preview_bug_shape


def collision_callback(arbiter, space, data):
    bugs = [bug for bug in arbiter.shapes if isinstance(bug, pymunk.Circle) and bug.body.body_type != 1]
    if len(bugs) > 1:
        if bugs[0].radius == bugs[1].radius:
            pos = bugs[0].body.position
            radius = bugs[0].radius
            next_grade = grades.next_grade(radius)
            space.remove(*bugs)
            create_bug(space, pos, next_grade, is_new=False)
    return True

