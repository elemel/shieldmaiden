from pygame.math import Vector2
from shieldmaiden.component import Component


class TransformComponent(Component):
    def __init__(self, entity=None, position=None):
        super().__init__(entity)
        self.position = Vector2()

        if position is not None:
            self.position.update(position)
