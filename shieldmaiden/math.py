from pygame.math import Vector2


def sign(a):
	return (0 < a) - (a < 0)


def move_toward(a, b, max_range):
	offset = b - a

	if abs(offset) <= max_range:
		return b

	return a + sign(offset) * max_range


def box_intersects_box(position_a: Vector2, size_a: Vector2, position_b: Vector2, size_b: Vector2) -> bool:
    left_a = position_a.x - 0.5 * size_a.x
    right_a = position_a.x + 0.5 * size_a.x
    top_a = position_a.y - 0.5 * size_a.y
    bottom_a = position_a.y + 0.5 * size_a.y

    left_b = position_b.x - 0.5 * size_b.x
    right_b = position_b.x + 0.5 * size_b.x
    top_b = position_b.y - 0.5 * size_b.y
    bottom_b = position_b.y + 0.5 * size_b.y

    return left_a < right_b and left_b < right_a and top_a < bottom_b and top_b < bottom_a
