class Component:
    def __init__(self, entity=None):
        self._entity = None

        if entity:
            self.entity = entity

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, entity):
        if entity != self.entity:
            if self.entity:
                del self.entity.scene.components[type(self)][id(self.entity)]
                del self.entity.components[type(self)]

            self._entity = entity

            if self.entity:
                self.entity.components[type(self)] = self
                self.entity.scene.components[type(self)][id(self.entity)] = self
