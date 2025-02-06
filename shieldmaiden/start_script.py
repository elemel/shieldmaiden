from pygame.math import Vector2

from shieldmaiden.entity import Entity
from shieldmaiden.box_component import BoxComponent
from shieldmaiden.maiden_script import MaidenScript
from shieldmaiden.script import Script
from shieldmaiden.script_component import ScriptComponent
from shieldmaiden.transform_component import TransformComponent


class StartScript(Script):
    def __init__(self, component=None):
        super().__init__(component)
        self.maiden = None

    def fixed_step(self, dt):
        if self.maiden is None or self.maiden.scene is None:
            transform_component = self.component.entity.components[TransformComponent]

            self.maiden = Entity(self.component.entity.scene)
            TransformComponent(self.maiden, transform_component.position)
            BoxComponent(self.maiden, Vector2(0.5, 1.5), (255, 127, 0))
            ScriptComponent(self.maiden, MaidenScript())
