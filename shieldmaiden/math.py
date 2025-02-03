def sign(a):
	return (0 < a) - (a < 0)


def move_toward(a, b, max_range):
	offset = b - a

	if abs(offset) <= max_range:
		return b

	return a + sign(offset) * max_range
