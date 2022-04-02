import math

from dataclasses import dataclass
from __future__ import annotations

from lights.color.rgb import RGBColor

@dataclass
class HSBColor:
    """A hue-saturation-brightness color (with each component in the range [0, 1])."""
    hue: float = 0
    saturation: float = 1
    brightness: float = 1

    @property
    def chroma(self) -> float:
        return self.brightness * self.saturation
    
    @property
    def as_rgb(self) -> RGBColor:
        """Converts this color to RGB."""
        # Source: https://en.wikipedia.org/wiki/HSL_and_HSV#HSV_to_RGB

        h = self.hue
        b = self.brightness
        c = self.chroma
        h_segment = math.floor(self.hue * 6)
        x = c * (1 - abs(h_segment % 2 - 1))

        if   h == 0: (r0, g0, b0) = (c, x, 0)
        elif h == 1: (r0, g0, b0) = (x, c, 0)
        elif h == 2: (r0, g0, b0) = (0, c, x)
        elif h == 3: (r0, g0, b0) = (0, x, c)
        elif h == 4: (r0, g0, b0) = (x, 0, c)
        else:        (r0, g0, b0) = (c, 0, x)

        m = b - c
        return RGBColor(r0 + m, g0 + m, b0 + m)

    def average(self, other: HSBColor) -> HSBColor:
        """The arithmetic mean of this and the given color."""
        return HSBColor((self.hue + other.hue) / 2, (self.saturation + other.saturation) / 2, (self.brightness + other.brightness) / 2)
    
    @property
    def norm(self) -> float:
        """The Euclidean norm of this color."""
        return math.sqrt(self.hue * self.hue + self.saturation * self.saturation + self.brightness * self.brightness)
    
    def distance(self, other: RGBColor) -> float:
        """The Euclidean distance to the specified color."""
        return (self - other).norm
    
    def approximately(self, other: RGBColor, eps: float = 0.001) -> bool:
        """Whether this color approximately equals the other."""
        return self.distance(other) < eps

    def __add__(self, other: HSBColor) -> HSBColor:
        if not isinstance(other, HSBColor):
            raise TypeError(f"Unsupported operand types for +: 'HSBColor' and '{type(other).__name__}'")
        return HSBColor(self.hue + other.hue, self.saturation + other.saturation, self.brightness + other.brightness)
    
    def __mul__(self, other: HSBColor) -> HSBColor:
        if not isinstance(other, float):
            raise TypeError(f"Unsupported operand types for *: 'HSBColor' and '{type(other).__name__}'")
        return HSBColor(self.hue * other, self.saturation * other, self.brightness * other)

    def __str__(self) -> str:
        return f"(hue={self.hue:.3f}, saturation={self.saturation:.3f}, brightness={self.brightness:.3f})"

HSB_COLORS = {
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
