#!/bin/bash

# Set env variables
export WAYLAND_DISPLAY="wayland-0"
export XDG_RUNTIME_DIR="/run/user/1000" # 1000 *should* be the user id. Beware

# Wait until HDMI is connected
echo "Testing hdmi"
until wlr-randr | grep "HDMI-A-1"; do
    echo "Waiting for HDMI input..."
    sleep 2
done

# Set the resolution lower. This may help. Idk to be honest.
/usr/bin/wlr-randr --output "HDMI-A-1" --mode 720x480@60

echo "HDMI input detected."

# Register the tv on port
cec-ctl -d /dev/cec0 --tv -S

# Disable HDMI out
wlopm --off "HDMI-A-1"

# Put TV into standby mode
cec-ctl -d /dev/cec0 --to 0 --standby
