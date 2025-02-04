import argparse
import pygame
from pygame.math import Vector2

from shieldmaiden.engine import Engine
from shieldmaiden.start import Start
from shieldmaiden.platform import Platform


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--height", type=int, default=600)
    parser.add_argument("--width", type=int, default=800)

    args = parser.parse_args()
    pygame.init()

    screen = pygame.display.set_mode((args.width, args.height), pygame.RESIZABLE | pygame.SCALED, vsync=1)
    pygame.display.set_caption("Shieldmaiden")

    engine = Engine()
    engine.after_add_group.connect(after_add_group)

    platform = Platform()
    platform.size.update(5.0, 0.5)
    engine.add_entity_tree(platform)

    start = Start()
    start.position.update(0.0, -1.125)
    engine.add_entity_tree(start)

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
            if hasattr(entity, "position") and hasattr(entity, "size") and hasattr(entity, "color"):
                rect_x = 0.5 * screen_width + camera_scale * (entity.position.x - 0.5 * entity.size.x)
                rect_y = 0.5 * screen_height + camera_scale * (entity.position.y - 0.5 * entity.size.y)

                rect_width = camera_scale * entity.size.x
                rect_height = camera_scale * entity.size.y

                rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                pygame.draw.rect(screen, entity.color, rect)

        # Update the display
        pygame.display.flip()

        clock.tick(args.fps)

    pygame.quit()


def after_add_group(group):
    print(f"Added group: {group.name}")

    def after_add_member(entity):
        print(f"Added entity @{id(entity)} to the {group.name} group")

    def before_remove_member(entity):
        print(f"Removing entity @{id(entity)} from the {group.name} group")

    group.after_add_member.connect(after_add_member, weak=False)
    group.before_remove_member.connect(before_remove_member, weak=False)


if __name__ == "__main__":
    main()
