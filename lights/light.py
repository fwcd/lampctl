from typing import List
from .color import HSBColor

class Light:
    @property
    def name(self) -> str:
        """Fetches the lamp's name."""
        return None

    @property
    def brightness(self) -> float:
        """Fetches the brightness of the lamp (on the range [0, 1])."""
        return None

    @brightness.setter
    def brightness(self, value: float):
        """Sets the brightness of the lamp (on the range [0, 1])."""
        raise NotImplementedError("Setting the brightness is not supported")

    @property
    def on(self) -> bool:
        """Whether the lamp is activated."""
        return None

    @on.setter
    def on(self, value: bool):
        """Activates or deactivates the lamp."""
        raise NotImplementedError("Activating or deactivating the lamp is not supported")

    def toggle(self):
        self.on = not self.on

    @property
    def color(self) -> HSBColor:
        """Fetches the RGB color of the lamp."""
        return None

    @color.setter
    def color(self, color: HSBColor):
        """Sets the RGB color of the lamp."""
        raise NotImplementedError("Setting the color is not supported")

    def __str__(self):
        return f"{self.name} (on={self.on}, brightness={self.brightness}, color={self.color})"

class LightSystem:
    def connect(self):
        """If required by the implementation, connects to the light system."""
        pass

    @property
    def lights(self) -> List[Light]:
        """Lists the available lights."""
        raise NotImplementedError("Cannot fetch lights")
    
    def lights_with_name(self, name: str) -> List[Light]:
        lights = [l for l in self.lights if l.name == name]
        if lights:
            return lights
        else:
            raise ValueError(f"No light with name {name} found")
