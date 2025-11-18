#!/bin/bash

# Set env variables
export WAYLAND_DISPLAY="wayland-0"
export XDG_RUNTIME_DIR="/run/user/1000" # 1000 should be the user id. Beware

# Wait until HDMI is connected
echo "Testing hdmi"
attempt=0
max_attempts=10
until wlr-randr | grep "HDMI-A-1"; do
    attempt=$((attempt + 1))
    if [ $attempt -ge $max_attempts ]; then
        echo "HDMI input not detected after $max_attempts attempts. Exiting."
        exit 0
    fi
    echo "Waiting for HDMI input... (Attempt $attempt/$max_attempts)"
    sleep 2
done
echo "HDMI input detected."

# Register the tv on port
cec-ctl -d /dev/cec0 --tv -S

# Enable HDMI out
wlopm --on "HDMI-A-1"

# Wake the TV
cec-ctl -d /dev/cec0 --to 0 --image-view-on

# Wait for the TV to fully turn on
max_retries=10
count=0

while [ $count -lt $max_retries ]; do
    pwr_state=$(cec-ctl -d/dev/cec0 --to 0 --give-device-power-status | grep -oP 'pwr-state:\s+\w+\s+\(\K[^)]+')
    echo "Attempt $((count + 1)): pwr-state = $pwr_state"

    if [ "$pwr_state" = "0x00" ]; then
        echo "Power state is ON (0x00)."
        break
    fi

    count=$((count + 1))
    sleep 1  # optional delay between retries
done

if [ $count -eq $max_retries ]; then
    echo "Max retries reached without detecting pwr-state 0x00."
fi

# Set the resolution
source ../autostart
