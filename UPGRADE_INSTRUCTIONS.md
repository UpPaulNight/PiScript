# Upgrade Instructions

## Commit 46a7a27

Fix possible race condition

### Steps for upgrade

1. `git stash/fetch/pull`
2. Create a virtual environment if you don't have one already:

    ```bash
    python3 -m venv .venv
    ```

3. Install the required packages:

    ```bash
    . .venv/bin/activate
    pip install -r requirements.txt
    ```

4. Copy the new service files into /etc/systemd/system and daemon-reload

## Commit 87e72a1

Switch to using python as the method to make sure the screen shuts on and off correctly

### Steps for upgrade

1. `cat` the autostart file at ~/.config/labwc/autostart and note the mode and
   transform values
2. `rm` the existing autostart file
3. `git stash/fetch/pull`
4. Edit the scripts/config.py file and fill in

    ```python
    mode = '3840x2160@24'
    transform = '270'
    ```

    with the values you noted in step 1
5. `cp` the service files into /etc/systemd/system
6. `systemctl daemon-reload`
7. Schedule a restart for later today at 17:10

### Commands to run

```bash
cat ~/.config/labwc/autostart
rm ~/.config/labwc/autostart
git stash
git fetch
git pull
nano scripts/config.py
sudo cp services/* /etc/systemd/system/
sudo systemctl daemon-reload
sudo shutdown -r 17:10
```
