from __future__ import annotations
from typing import Optional


class Entity:
	engine: Optional[Engine] = None

	parent: Optional[Entity] = None
	children: dict[int, Entity]
	group_names = dict[str, bool]

	def __init__(self) -> None:
		self.children = {}
		self.group_names = {}

	def add_group_name(self, name):
		if name in self.group_names:
			raise Exception(f"Group name was already added: {name}")

		self.group_names[name] = True

		if self.engine:
			self.engine.get_group(name).add_member(self)

	def remove_group_name(self, name):
		if name not in self.groups:
			raise Exception(f"Group name was never added: {name}")

		if self.engine:
			self.engine.get_group(name).remove_member(self)

		del self.group_names[name]
