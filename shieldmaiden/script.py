class Script:
    def __init__(self, component=None):
        self._component = None
        self.component = component

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, component):
        if component != self.component:
            if self.component:
                self.component._script = None

            self._component = component

            if self.component:
                self.component._script = self
