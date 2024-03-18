from lampctl.system import Lamp, LampSystem

class CombinedLampSystem(LampSystem):
    def __init__(self, systems: list[LampSystem] = []):
        self.systems = systems
    
    def add(self, system: LampSystem):
        self.systems.append(system)
    
    def connect(self):
        for system in self.systems:
            system.connect()
    
    @property
    def lamps(self) -> list[Lamp]:
        return [l for s in self.systems for l in s.lamps]
