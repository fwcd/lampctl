import argparse
import os
from typing import List

from lights.combined import CombinedLightSystem
from lights.light import Light, LightSystem
from lights.color import COLORS
from lights.hue import HueSystem

class CommandParams:
    def __init__(self, lights: List[Light], system: LightSystem, args: List[str]):
        self.lights = lights
        self.system = system
        self.args = args

def list_command(p: CommandParams):
    print("\n".join(f"{l.name:>15} ({f'on={l.on}':<8}, brightness={l.brightness:.2f}, color={l.color})" for l in p.system.lights))

def on_command(p: CommandParams):
    for light in p.lights:
        light.on = True

def off_command(p: CommandParams):
    for light in p.lights:
        light.on = False

def dim_command(p: CommandParams):
    try:
        arg = float(p.args[0])
    except:
        raise ValueError("Please enter an integer between 0 and 100!")

    for light in p.lights:
        light.brightness = arg / 100

def color_command(p: CommandParams):
    try:
        color = COLORS[p.args[0]]
    except:
        raise ValueError(f"Unrecognized color, try one of these: {', '.join(COLORS.keys)}")

    for light in p.lights:
        light.color = color

def toggle_command(p: CommandParams):
    for light in p.lights:
        light.toggle()

COMMANDS = {
    "list": list_command,
    "on": on_command,
    "off": off_command,
    "toggle": toggle_command,
    "dim": dim_command,
    "color": color_command
}

def main():
    parser = argparse.ArgumentParser(description="Lets you control your smart lamps at home.")
    parser.add_argument("-b", "--hue_bridge_ip", type=str, help="The IP of your Hue bridge.")
    parser.add_argument("-n", "--name", type=str, help="Optionally a single, selected light's name. By default, all lights are selected.")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="The command to invoke.")

    args = parser.parse_args()
    hue_bridge_ip = args.hue_bridge_ip or os.environ.get("LIGHTS_HUE_BRIDGE_IP")
    name = args.name or os.environ.get("LIGHTS_NAME")
    command = args.command

    # Setup light system
    selected = []
    system = CombinedLightSystem()

    if hue_bridge_ip:
        system.add(HueSystem(hue_bridge_ip))
    
    system.connect()

    if name:
        selected = system.lights_with_name(name)
    else:
        selected = system.lights

    # Perform user-invoked command
    if command:
        f = COMMANDS.get(command[0], None)
        if f:
            f(CommandParams(selected, system, command[1:]))
        else:
            print(f"Unrecognized command name {command[0]}. Try one of these: {', '.join(COMMANDS.keys())}")
    else:
        print(f"Unrecognized command invocation: {command}")

