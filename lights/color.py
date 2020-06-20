class Color:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

COLORS = {
    "red": Color(0xFF, 0, 0),
    "green": Color(0, 0xFF, 0),
    "blue": Color(0, 0, 0xFF),
    "magenta": Color(0xFF, 0, 0xFF),
    "cyan": Color(0, 0xFF, 0xFF),
    "yellow": Color(0xFF, 0xFF, 0),
    "white": Color(0xFF, 0xFF, 0xFF),
    "black": Color(0, 0, 0)
}
