import subprocess
from time import sleep
from get_logger import get_logger

logger = get_logger(__name__)

def register_tv(env: dict) -> bool:
    # Register the tv on port

    # Equivalent of `cec-ctl -d /dev/cec0 --tv -S`
    result = subprocess.run(['/usr/bin/cec-ctl', '-d', '/dev/cec0', '--tv', '-S'], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error("Failed to register TV.")
        logger.error(result.stderr.strip())
        return False
    return True

def power_on_tv(env: dict) -> bool:
    # Wake the TV

    # Equivalent of running `cec-ctl -d /dev/cec0 --to 0 --image-view-on`
    result = subprocess.run(['/usr/bin/cec-ctl', '-d', '/dev/cec0', '--to', '0', '--image-view-on'], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error("Failed to power on TV.")
        logger.error(result.stderr.strip())
        return False
    return True

def power_off_tv(env: dict) -> bool:
    # Put the TV to sleep

    # Equivalent of running `cec-ctl -d /dev/cec0 --to 0 --standby`
    result = subprocess.run(['/usr/bin/cec-ctl', '-d', '/dev/cec0', '--to', '0', '--standby'], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error("Failed to power off TV.")
        logger.error(result.stderr.strip())
        return False
    return True

def is_tv_on(env: dict) -> bool:
    # Check if the TV is on

    # Equivalent of running `cec-ctl -d/dev/cec0 --to 0 --give-device-power-status | grep -oP 'pwr-state:\s+\w+\s+\(\K[^)]+'`
    result = subprocess.run(['/usr/bin/cec-ctl', '-d', '/dev/cec0', '--to', '0', '--give-device-power-status'], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error("Failed to get TV power status.")
        logger.error(result.stderr.strip())
        return False
    
    output = result.stdout
    for line in output.splitlines():
        if 'pwr-state:' in line:
            if 'on' in line:
                return True
            else:
                return False
                
    logger.error("Could not determine TV power status from output.")
    return False

def test_tv_on(env: dict, limit: int = 5) -> bool:
    # Test if the TV is on, retrying up to limit times

    for attempt in range(limit):
        if is_tv_on(env):
            return True
        logger.debug(f'TV is off, retrying... ({attempt + 1}/{limit})')
        sleep(2)
    
    return False
