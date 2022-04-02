from dataclasses import dataclass

@dataclass
class RGBColor:
    """A red-green-blue color (with each component in the range [0, 1])."""
    red: float = 0
    green: float = 0
    blue: float = 0

    def average(self, other):
        return RGBColor((self.red + other.red) / 2, (self.green + other.green) / 2, (self.blue + other.blue) / 2)
    
    def __add__(self, other):
        if not isinstance(other, RGBColor):
            raise TypeError(f"Unsupported operand types for +: 'RGBColor' and '{type(other).__name__}'")
        return RGBColor(self.red + other.red, self.green + other.green, self.blue + other.blue)
    
    def __mul__(self, other):
        if not isinstance(other, float):
            raise TypeError(f"Unsupported operand types for *: 'RGBColor' and '{type(other).__name__}'")
        return RGBColor(self.red * other, self.green * other, self.blue * other)

    def __str__(self):
        return f"(red={self.red:.3f}, green={self.green:.3f}, blue={self.blue:.3f})"

RGB_COLORS = {
    "white": RGBColor(red=1, green=1, blue=1),
    "gray": RGBColor(red=0.5, green=0.5, blue=0.5),
    "black": RGBColor(red=0, green=0, blue=0),
    "red": RGBColor(red=1, green=0, blue=0),
    "green": RGBColor(red=0, green=1, blue=0),
    "blue": RGBColor(red=0, green=0, blue=1),
    "magenta": RGBColor(red=1, green=0, blue=1),
    "cyan": RGBColor(red=0, green=1, blue=1),
    "yellow": RGBColor(red=1, green=1, blue=0)
}
