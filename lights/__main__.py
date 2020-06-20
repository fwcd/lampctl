import argparse
import re
from typing import List
from .light import LightSystem
from .hue import HueSystem

def list_command(args: List[str], systems: List[LightSystem]):
    print([l.name for s in systems for l in s.lights])

COMMANDS = {
    "list": list_command
}

def main():
    parser = argparse.ArgumentParser(description="Lets you control your smart lamps at home.")
    parser.add_argument("-b", "--hue_bridge_ip", type=str, help="The IP of your Hue bridge.")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="The command to invoke.")

    args = parser.parse_args()
    command = args.command
    systems = []

    if args.hue_bridge_ip:
        systems.append(HueSystem(args.hue_bridge_ip))

    for system in systems:
        system.connect()

    if command:
        f = COMMANDS.get(command[0], None)
        if f:
            f(command[1:], systems)
        else:
            print(f"Unrecognized command name {command[0]}. Try one of these: {', '.join(COMMANDS.keys())}")
    else:
        print(f"Unrecognized command invocation: {command}")

if __name__ == "__main__":
    main()
