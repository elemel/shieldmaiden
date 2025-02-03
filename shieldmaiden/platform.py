from shieldmaiden.box import Box
from shieldmaiden.entity import Entity


class Platform(Entity):
	box: Box
	color: tuple[int, int, int]

	def __init__(self):
		super().__init__()
		self.box = Box()
		self.color = 0, 127, 255
		self.add_to_group("platforms")
