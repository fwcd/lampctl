import argparse
import json
import os
import pathlib

from dataclasses import dataclass
from lights.combined import CombinedLightSystem
from lights.light import Light, LightSystem
from lights.color import COLORS
from lights.hue import HueSystem

@dataclass
class CommandParams:
    lights: list[Light]
    system: LightSystem
    args: list[str]

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
    if p.args:
        try:
            color = COLORS[p.args[0]]
        except:
            raise ValueError(f"Unrecognized color, try one of these: {', '.join(COLORS.keys())}")
    else:
        color = COLORS["default"]

    for light in p.lights:
        light.color = color

def toggle_command(p: CommandParams):
    for light in p.lights:
        light.toggle()

DEFAULT_CONFIG_PATH = pathlib.Path.home() / ".config" / "lights" / "config.json"

COMMANDS = {
    "list": list_command,
    "on": on_command,
    "off": off_command,
    "toggle": toggle_command,
    "dim": dim_command,
    "color": color_command
}

SYSTEMS = {
    "hue": lambda config: HueSystem(config["bridge-ip"])
}

def main():
    parser = argparse.ArgumentParser(description="Lets you control your smart lamps at home.")
    parser.add_argument("--config", type=str, required=not DEFAULT_CONFIG_PATH.exists(), default=str(DEFAULT_CONFIG_PATH), help="Path to a config.json file that can be used to configure lights.")
    parser.add_argument("-n", "--name", type=str, help="A single, selected light's name. If a default light is set in the config file, this argument can be omitted.")
    parser.add_argument("-a", "--all", action="store_true", help="Selects all lights.")
    parser.add_argument("command", type=str, choices=sorted(COMMANDS.keys()), help="The command to invoke.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to the command to invoke.")

    args = parser.parse_args()

    config = {}
    config_path = pathlib.Path(args.config)

    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.loads(f.read())

    name = args.name or os.environ.get("LIGHTS_NAME") or config.get("default-light", None)
    select_all = args.all
    command_name = args.command
    command_args = args.args

    # Set up light systems
    system = CombinedLightSystem()

    for system_config in config.get("systems", []):
        system_type = system_config["type"]
        if system_type not in SYSTEMS.keys():
            raise ValueError(f"Unkown system type '{system_type}', try one of these: {', '.join(SYSTEMS.keys())}")
        system.add(SYSTEMS[system_type](system_config))

    system.connect()

    # Select lamp
    selected = []
    if select_all:
        selected = system.lights
    elif name:
        selected = system.lights_with_name(name)
    else:
        print("Warning: No lights selected (you can set a specific light with -n or pick all with --all)")

    # Perform user-invoked command
    command = COMMANDS.get(command_name, None)
    command(CommandParams(selected, system, command_args))

