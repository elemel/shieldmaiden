from typing import Optional
from pygame.math import Vector2

from shieldmaiden.entity import Entity
from shieldmaiden.maiden import Maiden


class Start(Entity):
    position: Vector2
    maiden: Optional[Maiden] = None

    def __init__(self):
        super().__init__()
        self.position = Vector2()

    def fixed_step(self, dt) -> None:
        if self.maiden is None or self.maiden.engine is None:
            self.maiden = Maiden()
            self.maiden.position.update(self.position)
            self.engine.add_entity_tree(self.maiden)
