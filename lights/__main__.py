import argparse
from .hue import HueSystem

def main():
    parser = argparse.ArgumentParser(description="Lets you control your smart lamps at home.")
    parser.add_argument("-b", "--hue_bridge_ip", type=str, help="The IP of your Hue bridge.")
    parser.add_argument("command", help="The command to invoke.")

    args = parser.parse_args()
    command = args.command
    systems = []

    if args.hue_bridge_ip:
        systems.append(HueSystem(args.hue_bridge_ip))

    for system in systems:
        system.connect()

    if command == "list":
        print([l.name for s in systems for l in s.lights])
    else:
        print(f"Unrecognized command {command}")

if __name__ == "__main__":
    main()
