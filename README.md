# Lights

A small CLI utility for controlling your smart lamps at home.

![Icon](lights-icon.png)

Currently only Philips Hue lamps are supported, but adding support for other backends is easy.

## Usage

To use, first create the file `~/.config/lights/config.json` pointing to your light systems:

```json
{
  "systems": [
    {
      "type": "hue",
      "bridge-ip": "your.ip.here"
    }
  ],
  "default-light": "My Lamp"
}
```

> If no `default-light` is set you can use the environment variable `LIGHTS_NAME` or `-n` to specify the light to control.

Now you can use the CLI to control your lights. For example:

* `lights on`
* `lights off`
* `lights toggle`
* `lights color blue`
* `lights dim 50`
* `lights --all on`
* `lights -n "My Lamp" on`

## Development

* Optionally setup a virtual environment:
    * Create a venv using `python3 -m venv venv`
    * Activate the venv using `source venv/bin/activate`
* Make sure that Wheel is installed using `pip3 install wheel`
* Finally install the dependencies with `pip3 install -r requirements.txt`

## Installation

* First make sure you are not in a virtual environment
* Then run `pip3 install .`
* If your Python packages are available on your `PATH` you should now be able to invoke `lights` from anywhere
