from __future__ import annotations
import argparse
import pygame
from pygame.math import Vector2

from shieldmaiden.box_component import BoxComponent
from shieldmaiden.camera_component import CameraComponent
from shieldmaiden.entity import Entity
from shieldmaiden.goal_component import GoalComponent
from shieldmaiden.level_script import LevelScript
from shieldmaiden.platform_component import PlatformComponent
from shieldmaiden.scene import Scene
from shieldmaiden.script_component import ScriptComponent
from shieldmaiden.start_component import StartComponent
from shieldmaiden.transform_component import TransformComponent


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--height", type=int, default=600)
    parser.add_argument("--width", type=int, default=800)

    args = parser.parse_args()
    pygame.init()

    window = pygame.display.set_mode((args.width, args.height), pygame.RESIZABLE | pygame.SCALED, vsync=1)
    pygame.display.set_caption("Shieldmaiden")

    scene = Scene()

    scene.add_component_type(BoxComponent)
    scene.add_component_type(CameraComponent)
    scene.add_component_type(GoalComponent)
    scene.add_component_type(PlatformComponent)
    scene.add_component_type(ScriptComponent)
    scene.add_component_type(StartComponent)
    scene.add_component_type(TransformComponent)

    level = Entity(scene)
    TransformComponent(level)
    BoxComponent(level, Vector2(10.0, 10.0), (31, 31, 31))
    ScriptComponent(level, LevelScript())

    camera = Entity(scene)
    TransformComponent(camera)
    CameraComponent(camera)

    platform = Entity(scene)
    TransformComponent(platform)
    BoxComponent(platform, Vector2(5.0, 0.5), (0, 127, 255))
    PlatformComponent(platform)

    start = Entity(scene)
    TransformComponent(start, Vector2(0.0, -1.0))
    StartComponent(start)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle window close
                running = False

        window_width = window.get_width()
        window_height = window.get_height()

        window.fill((0, 0, 0))

        fixed_dt = 1 / args.fps

        for script_component in list(scene.component_columns[ScriptComponent].values()):
            if script_component.entity and script_component.script and hasattr(script_component.script, "fixed_step"):
                script_component.script.fixed_step(fixed_dt)

        [camera_component] = scene.component_columns[CameraComponent].values()
        camera_transform_component = camera_component.entity.components[TransformComponent]
        camera_position = camera_transform_component.position
        camera_scale = 0.1 * window_height

        for box_component in scene.component_columns[BoxComponent].values():
            transform_component = box_component.entity.components[TransformComponent]

            rect_x = 0.5 * window_width + camera_scale * (transform_component.position.x - 0.5 * box_component.size.x - camera_position.x)
            rect_y = 0.5 * window_height + camera_scale * (transform_component.position.y - 0.5 * box_component.size.y - camera_position.y)

            rect_width = camera_scale * box_component.size.x
            rect_height = camera_scale * box_component.size.y

            rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(window, box_component.color, rect)

        # Update the display
        pygame.display.flip()

        clock.tick(args.fps)

    pygame.quit()


if __name__ == "__main__":
    main()
