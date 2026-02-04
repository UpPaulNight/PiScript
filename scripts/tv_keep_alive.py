#!/usr/bin/env python3

from cec_ctl_commands import is_tv_on
from wlopm_commands import is_hdmi_enabled
from get_env import get_environment
from get_logger import get_logger
from sanity_checks import run_sanity_checks
from filelock import Timeout, FileLock

def test_alive():
    """
    Test if the TV is responding to CEC commands. By running this function
    periodically, (ideally) it will keep the TV in a 'hey someone is plugged in'
    state OR if nothing it will tell us exactly around when the TV stops
    responding.
    """

    logger = get_logger('tvAliveScript')

    # Sanity checks
    if not run_sanity_checks():
        logger.error("Sanity checks failed. Exiting.")
        exit(1)

    env = get_environment()

    # Create a mutual exclusion lock because I think running a few of these
    # commands simultaneously might have been causing issues.
    lock = FileLock('tv_lock.lock', timeout=120)
    try:
        with lock:
            # Get the power status of the TV
            logger.debug('Checking if TV is on...')
            on_status = is_tv_on(env)
            logger.debug(f'TV on status: {on_status}')

            # Get the HDMI output status
            logger.debug('Checking if HDMI output is enabled...')
            hdmi_status = is_hdmi_enabled(env)
            logger.debug(f'HDMI output enabled: {hdmi_status}')
    
    except Timeout:
        logger.critical('Could not acquire lock within 120 seconds. Something else must have failed catastrophically.')
        exit(1)

if __name__ == "__main__":
    test_alive()
