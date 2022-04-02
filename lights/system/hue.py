import phue

from lights.system import Light, LightSystem
from lights.color.hsb import HSBColor

HUE_FACTOR = 56635
SATURATION_FACTOR = 254
BRIGHTNESS_FACTOR = 254

class HueLight(Light):
    def __init__(self, hue_light):
        self.hue_light = hue_light
    
    @property
    def name(self) -> str:
        return self.hue_light.name

    @property
    def brightness(self) -> float:
        return float(self.hue_light.brightness) / BRIGHTNESS_FACTOR
    
    @brightness.setter
    def brightness(self, value: float):
        self.hue_light.brightness = int(value * BRIGHTNESS_FACTOR)
    
    @property
    def on(self) -> bool:
        return self.hue_light.on

    @on.setter
    def on(self, value: bool):
        self.hue_light.on = value
    
    @property
    def color(self) -> HSBColor:
        return HSBColor(
            float(self.hue_light.hue) / HUE_FACTOR,
            float(self.hue_light.saturation) / SATURATION_FACTOR,
            float(self.hue_light.brightness) / BRIGHTNESS_FACTOR
        )

    @color.setter
    def color(self, color: HSBColor):
        self.hue_light.hue = int(color.hue * HUE_FACTOR)
        self.hue_light.saturation = int(color.saturation * SATURATION_FACTOR)
        self.hue_light.brightness = int(color.brightness * BRIGHTNESS_FACTOR)
        
class HueSystem(LightSystem):
    def __init__(self, ip: str):
        self.bridge = phue.Bridge(ip)

    def connect(self):
        self.bridge.connect()

    @property
    def lights(self) -> list[Light]:
        return [HueLight(l) for l in self.bridge.lights]
