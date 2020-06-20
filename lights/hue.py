import phue
from typing import List
from .light import Light, LightSystem

BRIGHTNESS_FACTOR = 255

class HueLight(Light):
    def __init__(self, hue_light):
        self.hue_light = hue_light
    
    @property
    def name(self) -> str:
        return self.hue_light.name

    @property
    def brightness(self) -> float:
        return self.hue_light.brightness / BRIGHTNESS_FACTOR
    
    @brightness.setter
    def brightness(self, value: float):
        self.hue_light.brightness = value * BRIGHTNESS_FACTOR
    
    @property
    def on(self) -> bool:
        return self.hue_light.on

    @on.setter
    def on(self, value: bool):
        self.hue_light.on = value
    
    # @property
    # def color(self):
    #     return None

    # @color.setter
    # def color(self, color: Color):
        
class HueSystem(LightSystem):
    def __init__(self, ip: str):
        self.bridge = phue.Bridge(ip)

    def connect(self):
        self.bridge.connect()

    @property
    def lights(self) -> List[Light]:
        return [HueLight(l) for l in self.bridge.lights]
