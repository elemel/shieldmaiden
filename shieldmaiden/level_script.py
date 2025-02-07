from pygame.math import Vector2

from shieldmaiden.box_component import BoxComponent
from shieldmaiden.camera_component import CameraComponent
from shieldmaiden.entity import Entity
from shieldmaiden.maiden_script import MaidenScript
from shieldmaiden.math import box_intersects_box
from shieldmaiden.script import Script
from shieldmaiden.script_component import ScriptComponent
from shieldmaiden.start_component import StartComponent
from shieldmaiden.transform_component import TransformComponent


class LevelScript(Script):
    def __init__(self, component=None):
        super().__init__(component)
        self.maiden = None

    def fixed_step(self, dt):
        if self.maiden and self.maiden.scene:
            transform_component = self.component.entity.components[TransformComponent]
            box_component = self.component.entity.components[BoxComponent]

            maiden_transform_component = self.maiden.components[TransformComponent]
            maiden_box_component = self.maiden.components[BoxComponent]

            if not box_intersects_box(maiden_transform_component.position, maiden_box_component.size, transform_component.position, box_component.size):
                self.maiden.scene = None
                self.maiden = None

        if self.maiden is None or self.maiden.scene is None:
            [start_component] = self.component.entity.scene.component_columns[StartComponent].values()

            if start_component:
                start_transform_component = start_component.entity.components[TransformComponent]

                self.maiden = Entity(self.component.entity.scene)
                TransformComponent(self.maiden, start_transform_component.position)
                BoxComponent(self.maiden, Vector2(0.5, 1.5), (255, 127, 0))
                ScriptComponent(self.maiden, MaidenScript())

        if self.maiden and self.maiden.scene:
            [camera_component] = self.component.entity.scene.component_columns[CameraComponent].values()
            camera_transform_component = camera_component.entity.components[TransformComponent]
            maiden_transform_component = self.maiden.components[TransformComponent]
            camera_transform_component.position.update(maiden_transform_component.position)
