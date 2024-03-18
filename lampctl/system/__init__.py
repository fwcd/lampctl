from lampctl.color.hsb import HSBColor

class Lamp:
    @property
    def name(self) -> str:
        """Fetches the lamp's name."""
        return None

    @property
    def brightness(self) -> float:
        """Fetches the brightness of the lamp (on the range [0, 1])."""
        raise NotImplementedError("Fetching the brightness is not supported")

    @brightness.setter
    def brightness(self, value: float):
        """Sets the brightness of the lamp (on the range [0, 1])."""
        raise NotImplementedError("Setting the brightness is not supported")

    @property
    def transition_time(self) -> float:
        """Fetches the transitioning time of the lamp (in seconds)."""
        raise NotImplementedError("Fetching the transition time is not supported")

    @transition_time.setter
    def transition_time(self, value: float):
        """Sets the transition time of the lamp (in seconds)."""
        raise NotImplementedError("Setting the transition time is not supported")

    @property
    def on(self) -> bool:
        """Whether the lamp is activated."""
        return False

    @on.setter
    def on(self, value: bool):
        """Activates or deactivates the lamp."""
        raise NotImplementedError("Activating or deactivating the lamp is not supported")

    def toggle(self):
        self.on = not self.on

    @property
    def color(self) -> HSBColor:
        """Fetches the RGB color of the lamp."""
        raise NotImplementedError("Fetching the color is not supported")

    @color.setter
    def color(self, color: HSBColor):
        """Sets the RGB color of the lamp."""
        raise NotImplementedError("Setting the color is not supported")

    def __str__(self):
        return f"{self.name} (on={self.on}, brightness={self.brightness}, color={self.color})"

class LampSystem:
    def connect(self):
        """If required by the implementation, connects to the lamp system."""
        pass

    @property
    def lamps(self) -> list[Lamp]:
        """lists the available lamps."""
        raise NotImplementedError("Cannot fetch lamps")
    
    def lamps_with_name(self, name: str) -> list[Lamp]:
        lamps = [l for l in self.lamps if l.name == name]
        if lamps:
            return lamps
        else:
            raise ValueError(f"No lamp with name {name} found")
