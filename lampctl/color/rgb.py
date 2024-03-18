from __future__ import annotations
from dataclasses import dataclass

import math
import lampctl.color.hsb as hsb

@dataclass
class RGBColor:
    """A red-green-blue color (with each component in the range [0, 1])."""
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0

    def average(self, other: RGBColor) -> RGBColor:
        """The arithmetic mean of this and the given color."""
        return RGBColor((self.red + other.red) / 2.0, (self.green + other.green) / 2.0, (self.blue + other.blue) / 2.0)

    @property
    def as_hsb(self) -> hsb.HSBColor:
        """Converts this color to HSB space."""
        # Source: https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB

        r = self.red
        g = self.green
        b = self.blue
        x_max = max(r, g, b)
        x_min = min(r, g, b)
        c = x_max - x_min
        
        if c == 0:       h = 0
        elif x_max == r: h = (    (g - b) / c) / 6
        elif x_max == g: h = (2 + (b - r) / c) / 6
        elif x_max == b: h = (4 + (r - g) / c) / 6
        else:            raise ValueError("unreachable")

        s = 0 if x_max == 0 else c / x_max

        return hsb.HSBColor(h, s, x_max)
    
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
    "white":   RGBColor(red=1.0, green=1.0, blue=1.0),
    "gray":    RGBColor(red=0.5, green=0.5, blue=0.5),
    "black":   RGBColor(red=0.0, green=0.0, blue=0.0),
    "red":     RGBColor(red=1.0, green=0.0, blue=0.0),
    "green":   RGBColor(red=0.0, green=1.0, blue=0.0),
    "blue":    RGBColor(red=0.0, green=0.0, blue=1.0),
    "magenta": RGBColor(red=1.0, green=0.0, blue=1.0),
    "cyan":    RGBColor(red=0.0, green=1.0, blue=1.0),
    "yellow":  RGBColor(red=1.0, green=1.0, blue=0.0)
}
