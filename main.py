import argparse
import pygame
from pygame.math import Vector2

from shieldmaiden.engine import Engine
from shieldmaiden.maiden import Maiden
from shieldmaiden.platform import Platform


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--height", type=int, default=600)
    parser.add_argument("--width", type=int, default=800)

    args = parser.parse_args()
    pygame.init()

    screen = pygame.display.set_mode((args.width, args.height), pygame.RESIZABLE)
    pygame.display.set_caption("Shieldmaiden")

    engine = Engine()
    engine.add_group("platforms")

    platform = Platform()
    platform.box.size = Vector2(5.0, 0.5)
    engine.add_entity_tree(platform)

    maiden = Maiden()
    maiden.box.center = Vector2(0.0, -1.125)
    engine.add_entity_tree(maiden)

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
        engine.fixed_step.send(fixed_dt)

        camera_scale = 0.1 * screen_height

        for entity in engine.entities.values():
            rect_x = 0.5 * screen_width + camera_scale * (entity.box.center.x - 0.5 * entity.box.size.x)
            rect_y = 0.5 * screen_height + camera_scale * (entity.box.center.y - 0.5 * entity.box.size.y)

            rect_width = camera_scale * entity.box.size.x
            rect_height = camera_scale * entity.box.size.y

            rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(screen, entity.color, rect)

        # Update the display
        pygame.display.flip()

        clock.tick(args.fps)

    pygame.quit()


if __name__ == "__main__":
    main()
