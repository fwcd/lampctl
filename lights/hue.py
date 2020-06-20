import phue
from typing import List
from .light import Light, LightSystem

class HueLight(Light):
    def __init__(self, hue_light):
        self.hue_light = hue_light
    
    @property
    def name(self) -> str:
        return self.hue_light.name

    @property
    def brightness(self) -> float:
        return self.hue_light.brightness
    
    @brightness.setter
    def brightness(self, value: float):
        self.hue_light.brightness = value
    
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
