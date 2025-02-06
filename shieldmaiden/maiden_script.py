import pygame
from pygame.math import Vector2

from shieldmaiden.box_component import BoxComponent
from shieldmaiden.entity import Entity
from shieldmaiden.math import sign, move_toward, box_intersects_box
from shieldmaiden.platform_component import PlatformComponent
from shieldmaiden.script import Script
from shieldmaiden.transform_component import TransformComponent


class MaidenScript(Script):
    def __init__(self, component=None):
        super().__init__(component)
        self.velocity = Vector2()

        self.walk_speed = 2.0
        self.walk_acceleration = 10.0

        self. jump_speed = 5.0
        self.fall_acceleration = 10.0

        self.jump_input = False
        self.on_ground = False

    def fixed_step(self, dt):
        transform_component = self.component.entity.components[TransformComponent]
        box_component = self.component.entity.components[BoxComponent]

        if transform_component.position.y > 10.0:
            self.component.entity.scene = None
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
        transform_component.position += self.velocity * dt

        self.on_ground = False

        for platform_component in self.component.entity.scene.components[PlatformComponent].values():
            platform_transform_component = platform_component.entity.components[TransformComponent]
            platform_box_component = platform_component.entity.components[BoxComponent]

            if box_intersects_box(transform_component.position, box_component.size, platform_transform_component.position, platform_box_component.size):
                transform_component.position.y = platform_transform_component.position.y - 0.5 * platform_box_component.size.y - 0.5 * box_component.size.y
                self.velocity.y = 0.0
                self.on_ground = True

        self.jump_input = jump_input
