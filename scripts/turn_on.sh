#!/bin/bash

# Set env variables
export WAYLAND_DISPLAY="wayland-0"
export XDG_RUNTIME_DIR="/run/user/1000" # 1000 should be the user id. Beware

# Wait until HDMI is connected
echo "Testing hdmi"
until wlr-randr | grep "HDMI-A-1"; do
    echo "Waiting for HDMI input..."
    sleep 2
done

echo "HDMI input detected."

# Register the tv on port
cec-ctl -d /dev/cec0 --tv -S

# Enable HDMI out
wlopm --on "HDMI-A-1"

# Wake the TV
cec-ctl -d /dev/cec0 --to 0 --image-view-on

source ../autostart
