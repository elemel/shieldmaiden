class Component:
    def __init__(self, entity=None):
        self._entity = None
        self.entity = entity

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, entity):
        if entity != self.entity:
            if entity and type(self) not in entity.scene.component_columns:
                raise Exception("Invalid component")

            if entity and type(self) in entity.components:
                raise Exception("Duplicate component")

            if self.entity:
                del self.entity.scene.component_columns[type(self)][id(self.entity)]
                del self.entity.components[type(self)]

            self._entity = entity

            if self.entity:
                self.entity.components[type(self)] = self
                self.entity.scene.component_columns[type(self)][id(self.entity)] = self
