class Entity:
    def __init__(self, engine=None, parent=None):
        self._engine = None
        self._parent = None
        self.children = {}
        self.components = {}
        self.engine = engine
        self.parent = parent

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, engine):
        if engine != self.engine:
            if self._engine:
                if self.children:
                    for child in reversed(list(self.children.values())):
                        child.parent = None

                if self.components:
                    for component in reversed(list(self.components.values())):
                        component.entity = None

                self.parent = None
                del self.engine.entities[id(self)]

            self._engine = engine

            if self.engine:
                self.engine.entities[id(self)] = self

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if parent != self.parent:
            if self.parent:
                del self.parent.children[id(self)]

            if parent and parent.engine != self.engine:
                self.engine = parent.engine

            self._parent = parent

            if self.parent:
                self.parent.children[id(self)] = self
