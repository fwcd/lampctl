import unittest

from lights.color.hsb import HSB_COLORS
from lights.color.rgb import RGB_COLORS

class TestColors(unittest.TestCase):
    def test_hsb_to_rgb(self):
        self.assertApproximately(HSB_COLORS["white"].as_rgb, RGB_COLORS["white"])
        self.assertApproximately(HSB_COLORS["red"].as_rgb, RGB_COLORS["red"])
        self.assertApproximately(HSB_COLORS["green"].as_rgb, RGB_COLORS["green"])
        self.assertApproximately(HSB_COLORS["yellow"].as_rgb, RGB_COLORS["yellow"])
        self.assertApproximately(HSB_COLORS["blue"].as_rgb, RGB_COLORS["blue"])
        self.assertApproximately(HSB_COLORS["black"].as_rgb, RGB_COLORS["black"])
    
    def assertApproximately(self, lhs, rhs):
        self.assertTrue(lhs.approximately(rhs), f"{lhs} should approximately equal {rhs}")

if __name__ == "__main__":
    unittest.main()
