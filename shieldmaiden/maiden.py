import pygame
from pygame.math import Vector2

from shieldmaiden.box import Box
from shieldmaiden.entity import Entity
from shieldmaiden.math import sign, move_toward


class Maiden(Entity):
	box: Box
	color: tuple[int, int, int]

	walk_speed: float = 2.0
	walk_acceleration: float = 10.0

	jump_speed = 5.0
	fall_acceleration: float = 10.0

	jump_input: bool = False
	on_ground: bool = False

	def __init__(self) -> None:
		super().__init__()
		self.box = Box(size=Vector2(0.5, 1.75))
		self.color = 255, 127, 0
		self.velocity = Vector2()

	def fixed_step(self, dt) -> None:
		keys = pygame.key.get_pressed()
		jump_input = keys[pygame.K_SPACE]

		if jump_input and not self.jump_input and self.on_ground:
			self.velocity.y = -self.jump_speed
			self.on_ground = False

		input_x = keys[pygame.K_d] - keys[pygame.K_a]

		if self.on_ground:
			target_velocity_x = input_x * self.walk_speed
			self.velocity.x = move_toward(self.velocity.x, target_velocity_x, self.walk_acceleration * dt)

		self.velocity.y += self.fall_acceleration * dt
		self.box.center += self.velocity * dt

		self.on_ground = False

		for platform in self.engine.groups["platforms"].values():
			if self.box.intersects(platform.box):
				self.box.center.y = platform.box.center.y - 0.5 * platform.box.size.y - 0.5 * self.box.size.y
				self.velocity.y = 0.0
				self.on_ground = True

		self.jump_input = jump_input
