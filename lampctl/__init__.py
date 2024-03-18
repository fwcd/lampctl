from dataclasses import dataclass
from typing import Callable

import argparse
import json
import os
import pathlib

from lampctl.system import Lamp, LampSystem
from lampctl.system.combined import CombinedLampSystem
from lampctl.system.hue import HueSystem
from lampctl.color.hsb import HSBColor, HSB_COLORS

@dataclass
class Options:
    lamps: list[Lamp]
    system: LampSystem
    verbose: bool
    args: list[str]

# Helpers

def update_onoff(new_on: Callable[[bool], bool], opts: Options):
    for lamp in opts.lamps:
        lamp.on = new_on(lamp.on)

        if opts.verbose:
            print(f"{lamp.name} is now {'on' if lamp.on else 'off'}")

def update_brightnesses(new_brightness: Callable[[float], float], opts: Options):
    for lamp in opts.lamps:
        lamp.brightness = new_brightness(lamp.brightness)
    
        if opts.verbose:
            print(f"{lamp.name}'s brightness is now {lamp.brightness}")

def update_colors(new_color: Callable[[HSBColor], HSBColor], opts: Options):
    for lamp in opts.lamps:
        lamp.color = new_color(lamp.color)

        if opts.verbose:
            print(f"{lamp.name}'s color is now {lamp.color}")

def list_lamps(lamps: list[Lamp]):
    for lamp in lamps:
        print(f"{lamp.name:>15} ({f'on={lamp.on}':<8}, brightness={lamp.brightness:.2f}, color={lamp.color})")

# Commands

def list_command(opts: Options):
    list_lamps(opts.system.lamps)

def status_command(opts: Options):
    list_lamps(opts.lamps)

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
            color = HSB_COLORS[opts.args[0]]
        except:
            raise ValueError(f"Unrecognized color, try one of these: {', '.join(HSB_COLORS.keys())}")
    else:
        color = HSB_COLORS["default"]
    
    update_colors(lambda _: color, opts)

def temp_command(opts: Options):
    try:
        arg = float(opts.args[0])
    except:
        raise ValueError("Please specify an integer between 0 (cold) and 100 (warm)!")
    
    factor = arg / 100
    color = HSB_COLORS["cold"] * (1 - factor) + HSB_COLORS["warm"] * factor
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

DEFAULT_CONFIG_PATH = pathlib.Path.home() / ".config" / "lampctl" / "config.json"

# Main

def main():
    parser = argparse.ArgumentParser(description="Lets you control your smart lamps at home.")
    parser.add_argument("--config", type=str, required=not DEFAULT_CONFIG_PATH.exists(), default=str(DEFAULT_CONFIG_PATH), help="Path to a config.json file that can be used to configure lamps.")
    parser.add_argument("-n", "--name", type=str, help="A single, selected lamp's name. If a default lamp is set in the config file, this argument can be omitted.")
    parser.add_argument("-a", "--all", action="store_true", help="Selects all lamps.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Logs more verbosely.")
    parser.add_argument("-t", "--transition-time", type=float, help="The transition time in seconds.")
    parser.add_argument("command", type=str, choices=sorted(COMMANDS.keys()), help="The command to invoke.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for the command to invoke.")

    args = parser.parse_args()

    config = {}
    config_path = pathlib.Path(args.config)

    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.loads(f.read())

    name = args.name or os.environ.get("DEFAULT_LAMP") or config.get("default-lamp", None)
    select_all = args.all
    verbose = args.verbose
    command_name = args.command
    command_args = args.args
    transition_time = args.transition_time

    # Set up lamp systems
    system = CombinedLampSystem()

    for system_config in config.get("systems", []):
        system_type = system_config["type"]
        if system_type not in SYSTEMS.keys():
            raise ValueError(f"Unkown system type '{system_type}', try one of these: {', '.join(SYSTEMS.keys())}")
        system.add(SYSTEMS[system_type](system_config))

    system.connect()

    # Select lamp
    selected = []
    if select_all:
        selected = system.lamps
    elif name:
        selected = system.lamps_with_name(name)
    elif verbose:
        print("Warning: No lamps selected (you can set a specific lamp with -n or pick all with --all)")

    # Set transition times if specified
    if transition_time is not None:
        for lamp in selected:
            lamp.transition_time = transition_time

    # Perform user-invoked command
    command = COMMANDS.get(command_name, None)
    command(Options(selected, system, verbose, command_args))

