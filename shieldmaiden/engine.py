class Engine:
    def __init__(self):
        # {domain_type: domain}
        self.domains = {}

        # {entity_id: entity}
        self.entities = {}

        # {component_type: {entity_id: component}}
        self.component_columns = {}

    def add_component_type(self, component_type):
        if component_type in self.component_columns:
            raise Exception("Duplicate component type")

        self.component_columns[component_type] = {}
