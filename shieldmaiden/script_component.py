from shieldmaiden.component import Component


class ScriptComponent(Component):
    def __init__(self, entity=None, script=None):
        super().__init__(entity)
        self._script = None
        self.script = script

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, script):
        if script != self.script:
            if self.script:
                self.script._component = None

            self._script = script

            if self.script:
                self.script._component = self
