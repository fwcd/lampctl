import argparse
import json
import os
import pathlib

from dataclasses import dataclass
from typing import Callable

from lights.system import Light, LightSystem
from lights.system.combined import CombinedLightSystem
from lights.system.hue import HueSystem
from lights.utils.color import HSBColor, COLORS

@dataclass
class Options:
    lights: list[Light]
    system: LightSystem
    verbose: bool
    args: list[str]

# Helpers

def update_onoff(new_on: Callable[[bool], bool], opts: Options):
    for light in opts.lights:
        light.on = new_on(light.on)

        if opts.verbose:
            print(f"{light.name} is now {'on' if light.on else 'off'}")

def update_brightnesses(new_brightness: Callable[[float], float], opts: Options):
    for light in opts.lights:
        light.brightness = new_brightness(light.brightness)
    
        if opts.verbose:
            print(f"{light.name}'s brightness is now {light.brightness}")

def update_colors(new_color: Callable[[HSBColor], HSBColor], opts: Options):
    for light in opts.lights:
        light.color = new_color(light.color)

        if opts.verbose:
            print(f"{light.name}'s color is now {light.color}")

def list_lights(lights: list[Light]):
    for light in lights:
        print(f"{light.name:>15} ({f'on={light.on}':<8}, brightness={light.brightness:.2f}, color={light.color})")

# Commands

def list_command(opts: Options):
    list_lights(opts.system.lights)

def status_command(opts: Options):
    list_lights(opts.lights)

def on_command(opts: Options):
    update_onoff(lambda _: True, opts)

def off_command(opts: Options):
    update_onoff(lambda _: False, opts)

def toggle_command(opts: Options):
    update_onoff(lambda on: not on, opts)

def dim_command(opts: Options):
    try:
        arg = float(opts.args[0])
    except:
        raise ValueError("Please enter an integer between 0 and 100!")
    
    brightness = arg / 100
    update_brightnesses(lambda _: brightness, opts)

def color_command(opts: Options):
    if opts.args:
        try:
            color = COLORS[opts.args[0]]
        except:
            raise ValueError(f"Unrecognized color, try one of these: {', '.join(COLORS.keys())}")
    else:
        color = COLORS["default"]
    
    update_colors(lambda _: color, opts)

def temp_command(opts: Options):
    try:
        arg = float(opts.args[0])
    except:
        raise ValueError("Please specify an integer between 0 (cold) and 100 (warm)!")
    
    factor = arg / 100
    color = COLORS["cold"] * (1 - factor) + COLORS["warm"] * factor
    update_colors(lambda _: color, opts)

# Constants

COMMANDS = {
    "list": list_command,
    "status": status_command,
    "on": on_command,
    "off": off_command,
    "toggle": toggle_command,
    "dim": dim_command,
    "color": color_command,
    "temp": temp_command
}

SYSTEMS = {
    "hue": lambda config: HueSystem(config["bridge-ip"])
}

DEFAULT_CONFIG_PATH = pathlib.Path.home() / ".config" / "lights" / "config.json"

# Main

def main():
    parser = argparse.ArgumentParser(description="Lets you control your smart lamps at home.")
    parser.add_argument("--config", type=str, required=not DEFAULT_CONFIG_PATH.exists(), default=str(DEFAULT_CONFIG_PATH), help="Path to a config.json file that can be used to configure lights.")
    parser.add_argument("-n", "--name", type=str, help="A single, selected light's name. If a default light is set in the config file, this argument can be omitted.")
    parser.add_argument("-a", "--all", action="store_true", help="Selects all lights.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Logs more verbosely.")
    parser.add_argument("command", type=str, choices=sorted(COMMANDS.keys()), help="The command to invoke.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for the command to invoke.")

    args = parser.parse_args()

    config = {}
    config_path = pathlib.Path(args.config)

    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.loads(f.read())

    name = args.name or os.environ.get("LIGHTS_NAME") or config.get("default-light", None)
    select_all = args.all
    verbose = args.verbose
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
    elif verbose:
        print("Warning: No lights selected (you can set a specific light with -n or pick all with --all)")

    # Perform user-invoked command
    command = COMMANDS.get(command_name, None)
    command(Options(selected, system, verbose, command_args))

