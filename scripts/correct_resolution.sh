#!/bin/bash

# Set env variables
export WAYLAND_DISPLAY="wayland-0"
export XDG_RUNTIME_DIR="/run/user/1000" # 1000 *should* be the user id. Beware

# Test if HDMI is connected
echo "Testing hdmi"
if ! wlr-randr | grep -q "HDMI-A-1"; then
    echo "HDMI input not detected. Exiting."
    exit 0
fi

echo "HDMI input detected."

# Get current resolution
current_resolution=$(/usr/bin/wlr-randr | grep '(current)' | xargs)

# Expected resolution
expected_resolution="720x480 px, 60.000000 Hz (current)"

# Check if current resolution matches expected
if [ "$current_resolution" != "$expected_resolution" ]; then
    echo "Current resolution: $current_resolution"
    echo "Expected resolution: $expected_resolution"
    echo "Fixing resolution..."
    /usr/bin/wlr-randr --output "HDMI-A-1" --mode 720x480@60
    echo "Resolution corrected."
else
    echo "Resolution is already correct: $current_resolution"
fi

# Get current transform
current_transform=$(/usr/bin/wlr-randr | grep Transform | xargs)

# Expected transform
expected_transform="Transform: 180"

# Check if current transform matches expected
if [ "$current_transform" != "$expected_transform" ]; then
    echo "Current transform: $current_transform"
    echo "Expected transform: $expected_transform"
    echo "Fixing transform..."
    /usr/bin/wlr-randr --output "HDMI-A-1" --transform 180
    echo "Transform corrected."
else
    echo "Transform is already correct: $current_transform"
fi
