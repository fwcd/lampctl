import argparse
import re
from typing import List
from .combined import CombinedLightSystem
from .light import LightSystem
from .hue import HueSystem

def list_command(args: List[str], system: LightSystem):
    print([l.name for l in system.lights])

def intended_lights(args: List[str], system: LightSystem):
    if args:
        name = args[0]
        lights = [l for l in system.lights if l.name == name]
        if lights:
            return lights
        else:
            raise ValueError(f"No light with name {name} found")
    else:
        return system.lights

def on_command(args: List[str], system: LightSystem):
    for light in intended_lights(args, system):
        light.brightness = 1

def off_command(args: List[str], system: LightSystem):
    for light in intended_lights(args, system):
        light.brightness = 0

COMMANDS = {
    "list": list_command,
    "on": on_command,
    "off": off_command
}

def main():
    parser = argparse.ArgumentParser(description="Lets you control your smart lamps at home.")
    parser.add_argument("-b", "--hue_bridge_ip", type=str, help="The IP of your Hue bridge.")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="The command to invoke.")

    args = parser.parse_args()
    command = args.command
    system = CombinedLightSystem()

    if args.hue_bridge_ip:
        system.add(HueSystem(args.hue_bridge_ip))

    if command:
        f = COMMANDS.get(command[0], None)
        if f:
            f(command[1:], system)
        else:
            print(f"Unrecognized command name {command[0]}. Try one of these: {', '.join(COMMANDS.keys())}")
    else:
        print(f"Unrecognized command invocation: {command}")

if __name__ == "__main__":
    main()
