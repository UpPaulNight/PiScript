#!/bin/bash

NEW_USER="john"
PACKAGES=("v4l-utils", "cec-utils", "wlr-randr", "wlopm", "adduser", "git")

### NEW USER INFO
# Ask for a password
read -p "Enter a password for the john account: " password

# Confirm the name
read -p "You entered '$password'. Is this correct? (y/n): " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo "Confirmed. Using '$password'..."
else
    echo "Aborted."
    exit 1
fi

### UPDATES
# Update system
sudo apt update && sudo apt upgrade -y

# Install packages
sudo apt install -y "${PACKAGES[@]}"


### NEW USER AND LOGIN
# Create the user that will log in every time
sudo useradd --password $password -m john

# Set the new user to be the one that is auto-logged in
sed -i '/autologin-user/c\
autologin-user=john'


### TV SCRIPTS
# Schedule the TV scripts to run in a cron job
crontab cronjobs

### KIOSK SERVICE
# Clone the correct files
mkdir "/home/john/Downloads"
sudo -u john git clone "https://github.com/UpPaulNight/Gemba-Board-Site.git" "/home/john/Downloads/Gemba-Board-Site"

# Schedule some systemd scripts for the new user
mkdir -p /home/john/.config/systemd/user
cp service-files/browser-kiosk.service /home/john/.config/systemd/user
chown john /home/john/.config/systemd/user/browser-kiosk.service
sudo -u john systemctl --user enable browser-kiosk.service

echo "Done. Restart for changes to take effect."
