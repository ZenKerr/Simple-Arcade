from pygame import Surface, Vector2

from app.entities.star import Star


class Stars:
    __slots__ = ("stars",)

    stars: list[Star]

    def __init__(self):
        self.stars = []

    def reset(self):
        self.stars.clear()

    def draw(self, surface: Surface, offset: Vector2):
        for star in self.stars:
            star.draw(surface, offset)

    def update(self):
        for star in self.stars:
            star.update()

    def add(self, star: Star):
        self.stars.append(star)
