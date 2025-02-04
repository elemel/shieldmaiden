from blinker import Signal
from shieldmaiden.entity import Entity
from shieldmaiden.group import Group


class Engine:
    groups: dict[str, dict]
    entities: dict[int, Entity]

    step: Signal
    fixed_step: Signal
    after_add_group: Signal

    def __init__(self) -> None:
        self.groups = {}
        self.entities = {}

        self.step = Signal()
        self.fixed_step = Signal()
        self.after_add_group = Signal()

    def get_group(self, name):
        if name not in self.groups:
            group = Group(name)
            self.groups[name] = group
            self.after_add_group.send(group)

        return self.groups[name]

    def add_entity_tree(self, entity: Entity) -> None:
        if id(entity) in self.entities:
            raise Exception("Already added")

        if entity.engine:
            raise Exception("Entity already has engine")

        entity.engine = self
        self.entities[id(entity)] = entity

        for name in entity.group_names:
            self.get_group(name).add_member(entity)

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

        for name in reversed(entity.group_names.keys()):
            self.get_group(name).remove_member(entity)

        del self.entities[id(entity)]
        entity.engine = None
