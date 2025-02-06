class Scene:
    def __init__(self):
        # {domain_type: domain}
        self.domains = {}

        # {entity_id: entity}
        self.entities = {}

        # {component_type: {entity_id: component}}
        self.components = {}
