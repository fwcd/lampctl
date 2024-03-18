# Lampctl

[![Test](https://github.com/fwcd/lampctl/actions/workflows/test.yml/badge.svg)](https://github.com/fwcd/lampctl/actions/workflows/test.yml)

A small CLI utility for controlling smart lamps.

![Icon](icon.png)

Currently only Philips Hue lamps are supported, but adding support for other backends is easy.

## Usage

To use, first create the file `~/.config/lampctl/config.json` pointing to your lamp systems:

```json
{
  "systems": [
    {
      "type": "hue",
      "bridge-ip": "your.ip.here"
    }
  ],
  "default-lamp": "My Lamp"
}
```

> If no `default-lamp` is set you can use the environment variable `DEFAULT_LAMP` or `-n` to select a lamp to control.

Now you can use the CLI to control your lamps. For example:

```sh
lampctl on               # turn selected lamp on
lampctl off              # turn selected lamp off
lampctl toggle           # toggle selected lamps
lampctl color blue       # set selected lamps to blue
lampctl dim 50           # dim selected lamps to 50%
lampctl --all on         # turn all lamps on
lampctl list             # list all lamps
lampctl status           # list selected lamps
lampctl -n "My Lamp" on  # turn lamp with name `MyLamp` on
```

## Development

* Optionally setup a virtual environment:
    * Create a venv using `python3 -m venv venv`
    * Activate the venv using `source venv/bin/activate`
* Make sure that Wheel is installed using `pip3 install wheel`
* Finally install the dependencies with `pip3 install -r requirements.txt`
* Now you can run `lampctl` with `python3 -m lampctl ...`
* To run the test suite, invoke `python3 -m unittest` in this directory

## Installation

* First make sure you are not in a virtual environment
* Then run `pip3 install .`
* If your Python packages are available on your `PATH` you should now be able to invoke `lampctl` from anywhere
