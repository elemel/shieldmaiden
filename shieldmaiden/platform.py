from pygame.math import Vector2
from shieldmaiden.entity import Entity


class Platform(Entity):
	position: Vector2
	size: Vector2
	color: tuple[int, int, int]

	def __init__(self):
		super().__init__()
		self.position = Vector2()
		self.size = Vector2(1.0)
		self.color = 0, 127, 255
		self.add_group_name("platforms")
