from pygame.math import Vector2


class Box:
    center: Vector2
    size: Vector2

    def __init__(self, center: Vector2 = Vector2(0.0), size: Vector2 = Vector2(1.0)) -> None:
        self.center = Vector2(center)
        self.size = Vector2(size)

    def intersects(self, other: "Box") -> bool:
        left = self.center.x - 0.5 * self.size.x
        right = self.center.x + 0.5 * self.size.x
        top = self.center.y - 0.5 * self.size.y
        bottom = self.center.y + 0.5 * self.size.y

        other_left = other.center.x - 0.5 * other.size.x
        other_right = other.center.x + 0.5 * other.size.x
        other_top = other.center.y - 0.5 * other.size.y
        other_bottom = other.center.y + 0.5 * other.size.y

        return left < other_right and other_left < right and top < other_bottom and other_top < bottom
