class Entity:
	engine: "Engine" = None

	parent: "Entity" = None
	children: dict[int, "Entity"]
	groups = dict[str, bool]

	def __init__(self) -> None:
		self.children = {}
		self.groups = {}

	def add_to_group(self, group):
		if group in self.groups:
			raise Exception(f"Already added to group: {group}")

		if self.engine:
			if group not in self.engine.groups:
				raise Exception(f"No such group: {group}")

			self.engine.groups[group][id(self)] = self

		self.groups[group] = True

	def remove_from_group(self, group):
		if group not in self.groups:
			raise Exception(f"Not added to group: {group}")

		if self.engine:
			if group not in self.engine.groups:
				raise Exception(f"No such group: {group}")

			del self.engine.groups[group][id(self)]

		del self.groups[group]
