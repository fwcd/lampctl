import phue

from lampctl.system import Lamp, LampSystem
from lampctl.color.hsb import HSBColor

HUE_FACTOR = 56635
SATURATION_FACTOR = 254
BRIGHTNESS_FACTOR = 254

class HueLamp(Lamp):
    def __init__(self, hue_lamp: phue.Light):
        self.hue_lamp = hue_lamp
    
    @property
    def name(self) -> str:
        return self.hue_lamp.name

    @property
    def brightness(self) -> float:
        return float(self.hue_lamp.brightness) / BRIGHTNESS_FACTOR
    
    @brightness.setter
    def brightness(self, value: float):
        self.hue_lamp.brightness = int(value * BRIGHTNESS_FACTOR)

    @property
    def transition_time(self) -> float:
        return float(self.hue_lamp.transitiontime) / 10

    @transition_time.setter
    def transition_time(self, value: float):
        self.hue_lamp.transitiontime = int(value * 10)
    
    @property
    def on(self) -> bool:
        return self.hue_lamp.on

    @on.setter
    def on(self, value: bool):
        self.hue_lamp.on = value
    
    @property
    def color(self) -> HSBColor:
        return HSBColor(
            float(self.hue_lamp.hue) / HUE_FACTOR,
            float(self.hue_lamp.saturation) / SATURATION_FACTOR,
            float(self.hue_lamp.brightness) / BRIGHTNESS_FACTOR
        )

    @color.setter
    def color(self, color: HSBColor):
        self.hue_lamp.hue = int(color.hue * HUE_FACTOR)
        self.hue_lamp.saturation = int(color.saturation * SATURATION_FACTOR)
        self.hue_lamp.brightness = int(color.brightness * BRIGHTNESS_FACTOR)
        
class HueSystem(LampSystem):
    def __init__(self, ip: str):
        self.bridge = phue.Bridge(ip)

    def connect(self):
        self.bridge.connect()

    @property
    def lamps(self) -> list[Lamp]:
        return [HueLamp(l) for l in self.bridge.lamps]
