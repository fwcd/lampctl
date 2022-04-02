from __future__ import annotations
from dataclasses import dataclass

import math

@dataclass
class RGBColor:
    """A red-green-blue color (with each component in the range [0, 1])."""
    red: float = 0
    green: float = 0
    blue: float = 0

    def average(self, other: RGBColor) -> RGBColor:
        """The arithmetic mean of this and the given color."""
        return RGBColor((self.red + other.red) / 2, (self.green + other.green) / 2, (self.blue + other.blue) / 2)
    
    @property
    def norm(self) -> float:
        """The Euclidean norm of this color."""
        return math.sqrt(self.red * self.red + self.green * self.green + self.blue * self.blue)
    
    def distance(self, other: RGBColor) -> float:
        """The Euclidean distance to the specified color."""
        return (self - other).norm
    
    def approximately(self, other: RGBColor, eps: float = 0.001) -> bool:
        """Whether this color approximately equals the other."""
        return self.distance(other) < eps
    
    def __add__(self, other: RGBColor) -> RGBColor:
        if not isinstance(other, RGBColor):
            raise TypeError(f"Unsupported operand types for +: 'RGBColor' and '{type(other).__name__}'")
        return RGBColor(self.red + other.red, self.green + other.green, self.blue + other.blue)

    def __sub__(self, other: RGBColor) -> RGBColor:
        if not isinstance(other, RGBColor):
            raise TypeError(f"Unsupported operand types for -: 'RGBColor' and '{type(other).__name__}'")
        return RGBColor(self.red - other.red, self.green - other.green, self.blue - other.blue)
    
    def __mul__(self, other: RGBColor) -> RGBColor:
        if not isinstance(other, float):
            raise TypeError(f"Unsupported operand types for *: 'RGBColor' and '{type(other).__name__}'")
        return RGBColor(self.red * other, self.green * other, self.blue * other)

    def __str__(self) -> str:
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
