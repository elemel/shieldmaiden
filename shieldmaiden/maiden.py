import pygame
from pygame.math import Vector2

from shieldmaiden.entity import Entity
from shieldmaiden.math import sign, move_toward, box_intersects_box


class Maiden(Entity):
	position: Vector2
	size: Vector2
	velocity: Vector2

	color: tuple[int, int, int]

	walk_speed: float = 2.0
	walk_acceleration: float = 10.0

	jump_speed = 5.0
	fall_acceleration: float = 10.0

	jump_input: bool = False
	on_ground: bool = False

	def __init__(self) -> None:
		super().__init__()
		self.position = Vector2()
		self.size = Vector2(0.5, 1.5)
		self.velocity = Vector2()
		self.color = 255, 127, 0
		self.add_group_name("maiden")

	def fixed_step(self, dt) -> None:
		if self.position.y > 10.0:
			self.engine.remove_entity_tree(self)
			return

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
		self.position += self.velocity * dt

		self.on_ground = False

		for platform in self.engine.get_group("platforms").members.values():
			if box_intersects_box(self.position, self.size, platform.position, platform.size):
				self.position.y = platform.position.y - 0.5 * platform.size.y - 0.5 * self.size.y
				self.velocity.y = 0.0
				self.on_ground = True

		self.jump_input = jump_input
