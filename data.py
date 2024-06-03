from dataclasses import dataclass
import random

from config import MIN_MASS_BUG, MIN_RADIUS_BUG, NUM_START_BUG, UP_SIZE, COLORS_FOR_BUG


@dataclass(frozen=True, eq=True)
class Grade:
    color: tuple[int]
    radius: float
    mass: float

    def __str__(self):
        return f"{self.radius}"


class Grades(list):
    def __init__(self, *args):
        self.colors = (color for color in COLORS_FOR_BUG)
        super().__init__(*args)
        self.next_radius = MIN_RADIUS_BUG
        self.next_mass = MIN_MASS_BUG
        self.current_radius = 0
        for _ in range(NUM_START_BUG):
            self.add()

    def add(self, *args, **kwargs):
        grade = Grade(
            color=self._get_color(), radius=self.next_radius, mass=self.next_mass
        )
        self.current_radius = self.next_radius
        self.next_radius *= UP_SIZE
        self.next_mass *= UP_SIZE
        super().append(grade)
        return grade

    def _get_color(self) -> tuple:
        try:
            return next(self.colors)
        except StopIteration:
            self.colors = (color for color in COLORS_FOR_BUG)
            return next(self.colors)

    def get_ramdom_grade(self):
        k = len(self) - 1 if len(self) < 6 else 5
        items = list(self)[:k]
        return random.choice(items)

    def next_grade(self, radius):
        if radius == self.current_radius:
            return self.add()
        for grade in self:
            if grade.radius == radius * UP_SIZE:
                return grade


class Score:
    value = 0

    def add(self, x: int | float):
        self.value += int(x)

    def __str__(self):
        return str(self.value)


grades = Grades()

score = Score()
