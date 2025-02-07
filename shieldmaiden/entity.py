class Entity:
    def __init__(self, scene=None, parent=None):
        self._scene = None
        self._parent = None
        self.children = {}
        self.components = {}
        self.scene = scene
        self.parent = parent

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        if scene != self.scene:
            if self._scene:
                if self.children:
                    for child in reversed(list(self.children.values())):
                        child.parent = None

                if self.components:
                    for component in reversed(list(self.components.values())):
                        component.entity = None

                self.parent = None
                del self.scene.entities[id(self)]

            self._scene = scene

            if self.scene:
                self.scene.entities[id(self)] = self

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if parent != self.parent:
            if self.parent:
                del self.parent.children[id(self)]

            if parent and parent.scene != self.scene:
                self.scene = parent.scene

            self._parent = parent

            if self.parent:
                self.parent.children[id(self)] = self
