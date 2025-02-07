class Domain:
    def __init__(self, scene=None):
        self._scene = None
        self.scene = scene

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        if scene != self.scene:
            if scene and type(self) in scene.domains:
                raise Exception("Duplicate domain")

            if self.scene:
                del self.scene.domains[type(self)]

            self._scene = scene

            if self.scene:
                self.scene.domains[type(self)] = self
