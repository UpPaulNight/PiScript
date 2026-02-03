#!/bin/bash
set -euo pipefail

# Python environment setup
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt

# Copy service files
sudo cp services/* /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable correct_resolution.timer
sudo systemctl enable turn_tv_off.timer
sudo systemctl enable turn_tv_on.timer

sudo systemctl start correct_resolution.timer
sudo systemctl start turn_tv_off.timer
sudo systemctl start turn_tv_on.timer

echo "Installation complete."
