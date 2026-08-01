from collections.abc import Callable
from typing import TYPE_CHECKING

from pygame import Surface, Vector2

from app.entities.enemy import Enemy
from app.entities.player import Player

if TYPE_CHECKING:
    from app.data import Data


class Enemies:
    __slots__ = ("app_data", "enemies", "reset_timer", "timer")

    app_data: "Data"
    enemies: list[Enemy]
    reset_timer: Callable[[], float]
    timer: float

    def __init__(self, app_data: "Data", reset_timer: Callable[[], float]):
        self.app_data = app_data

        self.enemies = []
        self.timer = reset_timer()
        self.reset_timer = reset_timer

    def reset(self):
        self.enemies.clear()

        self.timer = self.reset_timer()

    def draw(self, surface: Surface):
        for enemy in self.enemies:
            enemy.draw(surface)

    def update(self, target: Vector2, time_coefficient: float) -> int:
        self.timer -= time_coefficient

        if self.timer <= 0:
            self.enemies.append(Enemy(self.app_data, target))

            self.timer = self.reset_timer()

        deleted = 0
        for i in range(len(self.enemies) - 1, -1, -1):
            enemy = self.enemies[i]

            enemy.update(time_coefficient)

            if enemy.wait_delete:
                deleted += 1

                del self.enemies[i]

        return deleted

    def check_player_collision(self, player: Player) -> bool:
        for enemy in self.enemies:
            squared_distance = enemy.position.distance_squared_to(player.position)
            if squared_distance <= (enemy.radius + player.radius) ** 2:
                return True

        return False

    def on_click(self, mouse_position: Vector2) -> Enemy | None:
        for i, enemy in enumerate(self.enemies):
            for segment in enemy.tail.get_segments():
                squared_distance = segment.position.distance_squared_to(mouse_position)

                if squared_distance < segment.radius**2:
                    return self.enemies.pop(i)

        return None
