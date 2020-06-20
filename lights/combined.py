from typing import List
from .light import Light, LightSystem

class CombinedLightSystem(LightSystem):
    def __init__(self, systems: List[LightSystem] = []):
        self.systems = systems
    
    def add(self, system: LightSystem):
        self.systems.append(system)
    
    def connect(self):
        for system in self.systems:
            system.connect()
    
    @property
    def lights(self) -> List[Light]:
        return [l for s in self.systems for l in s.lights]
