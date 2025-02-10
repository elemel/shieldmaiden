class Domain:
    def __init__(self, engine=None):
        self._engine = None
        self.engine = engine

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, engine):
        if engine != self.engine:
            if engine and type(self) in engine.domains:
                raise Exception("Duplicate domain")

            if self.engine:
                del self.engine.domains[type(self)]

            self._engine = engine

            if self.engine:
                self.engine.domains[type(self)] = self
