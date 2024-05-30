from dataclasses import dataclass
import random

from config import MIN_MASS_BUG, MIN_RADIUS_BUG, NUM_START_BUG, UP_SIZE


@dataclass(frozen=True, eq=True)
class Grade:
    color: tuple[int]
    radius: float
    mass: float


class Grades(set):
    def __init__(self, *args):
        super().__init__(*args)
        self.next_radius = MIN_RADIUS_BUG
        self.next_mass = MIN_MASS_BUG
        self.current_radius = 0
        for _ in range(NUM_START_BUG):
            self.add()

    def add(self, *args, **kwargs):
        grade = Grade(color=self._get_random_color(), radius=self.next_radius, mass=self.next_mass)
        self.current_radius = self.next_radius
        self.next_radius *= UP_SIZE
        self.next_mass *= UP_SIZE
        super().add(grade)
        return grade

    @staticmethod
    def _get_random_color() -> tuple:
        return tuple(random.randrange(256) for i in range(4))

    def get_ramdom_grade(self):
        return random.choice(list(self)[:-1])

    def next_grade(self, radius):
        if radius == self.current_radius:
            return self.add()
        for grade in self:
            if grade.radius == radius * UP_SIZE:
                return grade

grades = Grades()
