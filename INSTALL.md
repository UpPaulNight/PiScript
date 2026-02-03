# Install Instructions

## Prerequisites

There are certain parts of this process (for testing and installation) that
require the TV you want to set this up for to be connected to the Raspberry Pi
and turned ON. If you already know the values you want to use for your setup,
you can skip this step.

### Configuration

In the scripts folder, create a `config.py` file with the following contents:

```python
mode = '3840x2160@24'  # Set your desired screen mode
transform = '270'      # Set your desired screen rotation
```

Replace the values with numbers that make sense for your setup. To get a list of
allowed modes run `wlr-randr`. Transform can be one of `normal`, `90`, `180`,
`270` where `normal` means no rotation.

### Selecting a resolution mode

Different pages are designed to work at different 4K resolutions. First figure
out if it is designed to be vertical or horizontal. When you know that, find out
if the page was designed to take up the full 4K resolution of 4096x2160 or if it
was designed for 3840x2160. A high resolution will usually work fine and not
look any different, but picking the lowest resolution will make both the
Raspberry Pi and the TV last longer.

All of the current TVs support up to 30 Hz, but you should pick the lowest one
available. Unless high quality animations are being displayed, the difference
between 24 and 30 Hz is literally nonexistent because these are static pages.

## Installation

### Install required packages

Python packages and environment setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Service files

Copy the service files to the systemd directory

```bash
sudo cp services/* /etc/systemd/system/
sudo systemctl daemon-reload
```

Enable and start the timers

```bash
sudo systemctl enable correct_resolution.timer
sudo systemctl enable turn_tv_off.timer
sudo systemctl enable turn_tv_on.timer

sudo systemctl start correct_resolution.timer
sudo systemctl start turn_tv_off.timer
sudo systemctl start turn_tv_on.timer
```

### VS Code Tunnels

To install VS Code and set up a tunnel that runs on startup, first install it by
following the instructions at [VS Code
Tunnels](https://code.visualstudio.com/docs/remote/tunnels).

Next enable and start the service

```bash
sudo systemctl enable start_vscode_tunnel.service
sudo systemctl start start_vscode_tunnel.service
```

There is a one-time startup process to actually get the tunnel started. Look at
the log of the service to get the URL to connect to

```bash
sudo systemctl status start_vscode_tunnel.service
```

It'll say there is a URL to go to and a 8 character code to enter. Do that and
then it'll connect every time.

Some environment variables that I use during development that deal with displays
don't show up with the profile that VS Code uses when you launch a terminal
there. These are related to the display server and dbus. Instead of editing the
bash profile scripts, I think it is simpler just to set them in the VS Code
settings. Add the following to the "device" settings.json in VS Code:

```json
"terminal.integrated.env.linux": {
    "XDG_RUNTIME_DIR": "/run/user/1000",
    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
    "WAYLAND_DISPLAY": "wayland-0"
}
```

This will ensure that the terminal in VS Code can interact with the display
server and will solve a lot of headaches preemptively.
