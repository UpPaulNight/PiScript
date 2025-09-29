#!/bin/bash

# Set env variables
export WAYLAND_DISPLAY="wayland-0"

# Wait until HDMI is connected
echo "Testing hdmi"
until wlr-randr | grep "HDMI-A-1"; do
    echo "Waiting for HDMI input..."
    sleep 2
done

echo "HDMI input detected."

# Register the tv on port
cec-ctl -d /dev/cec0 --tv -S

# Disable HDMI out
wlopm --off "HDMI-A-1"

# Put TV into standby mode
cec-ctl -d /dev/cec0 --to 0 --standby
