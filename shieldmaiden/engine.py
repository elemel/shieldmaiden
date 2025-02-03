from blinker import signal
from shieldmaiden.entity import Entity


class Engine:
    groups: dict[str, dict]
    entities: dict[int, Entity]

    step: signal
    fixed_step: signal

    def __init__(self) -> None:
        self.groups = {}
        self.entities = {}

        self.step = signal("step")
        self.fixed_step = signal("fixed_step")

    def add_group(self, group):
        if group in self.groups:
            raise Exception(f"Group already exists: {group}")

        self.groups[group] = {}

    def remove_group(self, group):
        if group not in self.groups:
            raise Exception(f"No such group: {group}")

        if self.groups[group]:
            raise Exception(f"Group is not empty: {group}")

        del self.groups[group]

    def add_entity_tree(self, entity: Entity) -> None:
        if id(entity) in self.entities:
            raise Exception("Already added")

        if entity.engine:
            raise Exception("Entity already has engine")

        entity.engine = self
        self.entities[id(entity)] = entity

        for group in entity.groups:
            if group not in self.groups:
                raise Exception(f"No such group: {group}")

            self.groups[group][id(entity)] = entity

        if hasattr(entity, "step"):
            self.step.connect(entity.step)

        if hasattr(entity, "fixed_step"):
            self.fixed_step.connect(entity.fixed_step)

        if hasattr(entity, "before_add_to_engine"):
            entity.before_add_to_engine()

        for child in entity.children.values():
            self.add_entity_tree(child)

        if hasattr(entity, "after_add_to_engine"):
            entity.after_add_to_engine()

    def remove_entity_tree(self, entity: Entity) -> None:
        if id(entity) not in self.entities:
            raise Exception("Not added")

        if hasattr(entity, "before_remove_from_engine"):
            entity.before_remove_from_engine()

        for child in reversed(entity.children.values()):
            self.remove_entity_tree(child)

        if hasattr(entity, "after_remove_from_engine"):
            entity.after_remove_from_engine()

        if hasattr(entity, "fixed_step"):
            self.fixed_step.disconnect(entity.fixed_step)

        if hasattr(entity, "step"):
            self.step.disconnect(entity.step)

        for group in entity.groups:
            if group not in self.groups:
                raise Exception(f"No such group: {group}")

            del self.groups[group][id(entity)]

        del self.entites[id(entity)]
        entity.engine = None
