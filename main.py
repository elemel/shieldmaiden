from __future__ import annotations
import argparse
import pygame
from pygame.math import Vector2

from shieldmaiden.box_component import BoxComponent
from shieldmaiden.entity import Entity
from shieldmaiden.platform_component import PlatformComponent
from shieldmaiden.scene import Scene
from shieldmaiden.script_component import ScriptComponent
from shieldmaiden.start_script import StartScript
from shieldmaiden.transform_component import TransformComponent


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--height", type=int, default=600)
    parser.add_argument("--width", type=int, default=800)

    args = parser.parse_args()
    pygame.init()

    screen = pygame.display.set_mode((args.width, args.height), pygame.RESIZABLE | pygame.SCALED, vsync=1)
    pygame.display.set_caption("Shieldmaiden")

    scene = Scene()

    scene.components[BoxComponent] = {}
    scene.components[PlatformComponent] = {}
    scene.components[ScriptComponent] = {}
    scene.components[TransformComponent] = {}

    platform = Entity(scene)
    TransformComponent(platform)
    BoxComponent(platform, Vector2(5.0, 0.5), (0, 127, 255))
    PlatformComponent(platform)

    start = Entity(scene)
    TransformComponent(start, Vector2(0.0, -1.0))
    ScriptComponent(start, StartScript())

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle window close
                running = False

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Fill the screen with a color (optional)
        screen.fill((0, 0, 0))

        fixed_dt = 1 / args.fps

        for script_component in list(scene.components[ScriptComponent].values()):
            if script_component.entity and script_component.script and hasattr(script_component.script, "fixed_step"):
                script_component.script.fixed_step(fixed_dt)

        camera_scale = 0.1 * screen_height

        for box_component in scene.components[BoxComponent].values():
            transform_component = box_component.entity.components[TransformComponent]

            rect_x = 0.5 * screen_width + camera_scale * (transform_component.position.x - 0.5 * box_component.size.x)
            rect_y = 0.5 * screen_height + camera_scale * (transform_component.position.y - 0.5 * box_component.size.y)

            rect_width = camera_scale * box_component.size.x
            rect_height = camera_scale * box_component.size.y

            rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(screen, box_component.color, rect)

        # Update the display
        pygame.display.flip()

        clock.tick(args.fps)

    pygame.quit()


if __name__ == "__main__":
    main()
