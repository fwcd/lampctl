import unittest

from lampctl.color.hsb import HSB_COLORS
from lampctl.color.rgb import RGB_COLORS

class TestColors(unittest.TestCase):
    def test_hsb_to_rgb(self):
        self.assertApproximately(HSB_COLORS["white"].as_rgb, RGB_COLORS["white"])
        self.assertApproximately(HSB_COLORS["red"].as_rgb, RGB_COLORS["red"])
        self.assertApproximately(HSB_COLORS["green"].as_rgb, RGB_COLORS["green"])
        self.assertApproximately(HSB_COLORS["yellow"].as_rgb, RGB_COLORS["yellow"])
        self.assertApproximately(HSB_COLORS["blue"].as_rgb, RGB_COLORS["blue"])
        self.assertApproximately(HSB_COLORS["black"].as_rgb, RGB_COLORS["black"])
    
    def test_rgb_hsb_conversion(self):
        for name, color in RGB_COLORS.items():
            self.assertApproximately(color.as_hsb.as_rgb, color, name)

    # TODO: HSB -> RGB conversion is not accurate enough yet to handle e.g.
    #       the warmer/colder whitetones

    # def test_hsb_rgb_conversion(self):
    #     for name, color in HSB_COLORS.items():
    #         self.assertApproximately(color.as_rgb.as_hsb, color, name)
    
    def assertApproximately(self, lhs, rhs, name=None):
        self.assertTrue(lhs.approximately(rhs), f"{lhs} should approximately equal {rhs} ({name or 'unnamed'})")

if __name__ == "__main__":
    unittest.main()
