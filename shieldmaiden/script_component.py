from shieldmaiden.component import Component


class ScriptComponent(Component):
    def __init__(self, entity=None, script=None):
        super().__init__(entity)
        self.script = script

        if self.script:
            self.script.component = self
