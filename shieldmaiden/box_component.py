from pygame.math import Vector2
from shieldmaiden.component import Component


class BoxComponent(Component):
    def __init__(self, entity=None, size=None, color=None):
        super().__init__(entity)
        self.size = Vector2(1.0)
        self.color = 255, 255, 255

        if size is not None:
            self.size.update(size)

        if color is not None:
            self.color = color
