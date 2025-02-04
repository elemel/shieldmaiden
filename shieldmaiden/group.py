from __future__ import annotations
from blinker import Signal


class Group:
    name: str
    members: dict[int, Entity]

    after_add_member: Signal
    before_remove_member: Signal

    def __init__(self, name):
        self.name = name
        self.members = {}

        self.after_add_member = Signal()
        self.before_remove_member = Signal()

    def add_member(self, entity):
        if id(entity) in self.members:
            raise Exception("Already added")

        self.members[id(entity)] = entity
        self.after_add_member.send(entity)

    def remove_member(self, entity):
        if id(entity) not in self.members:
            raise Exception("Not added")

        self.before_remove_member.send(entity)
        del self.members[id(entity)]
