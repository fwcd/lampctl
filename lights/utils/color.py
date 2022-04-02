from dataclasses import dataclass

@dataclass
class HSBColor:
    """A hue-saturation-brightness color."""
    hue: float = 0
    saturation: float = 1
    brightness: float = 1
    
    def average(self, other):
        return HSBColor((self.hue + other.hue) / 2, (self.saturation + other.saturation) / 2, (self.brightness + other.brightness) / 2)
    
    def __add__(self, other):
        if not isinstance(other, HSBColor):
            raise TypeError(f"Unsupported operand types for +: 'HSBColor' and '{type(other).__name__}'")
        return HSBColor(self.hue + other.hue, self.saturation + other.saturation, self.brightness + other.brightness)
    
    def __mul__(self, other):
        if not isinstance(other, float):
            raise TypeError(f"Unsupported operand types for *: 'HSBColor' and '{type(other).__name__}'")
        return HSBColor(self.hue * other, self.saturation * other, self.brightness * other)

    def __str__(self):
        return f"(hue={self.hue:.3f}, saturation={self.saturation:.3f}, brightness={self.brightness:.3f})"

COLORS = {
    "default": HSBColor(hue=0.149, saturation=0.551),
    "white": HSBColor(saturation=0, brightness=1),
    "warm": HSBColor(hue=0.127, saturation=0.886),
    "cold": HSBColor(hue=0.733, saturation=0.307),
    "black": HSBColor(saturation=0, brightness=0),
    "red": HSBColor(hue=0),
    "orange": HSBColor(hue=0.08),
    "yellow": HSBColor(hue=0.17),
    "green": HSBColor(hue=0.45),
    "blue": HSBColor(hue=0.82),
    "purple": HSBColor(hue=0.88)
}
