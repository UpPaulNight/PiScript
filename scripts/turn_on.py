#!/usr/bin/env python3

from wlr_randr_commands import wait_hdmi_input
from cec_ctl_commands import register_tv, power_on_tv, test_tv_on
from wlopm_commands import enable_hdmi_out
from get_env import get_environment
from get_logger import get_logger
from sanity_checks import run_sanity_checks
from correct_resolution import correct_resolution
from shut_down import reboot
from filelock import Timeout, FileLock

def turn_on():
    # I may be a little overzealous with rebooting on failure, but I am tired of
    # having to reboot these things manually when they won't start. So tada. I
    # do that here. Dear lord, I hate tvs

    logger = get_logger('turn_on script')

    # Sanity checks
    if not run_sanity_checks():
        logger.error("Sanity checks failed. Exiting.")
        exit(1)

    env = get_environment()

    # Create a mutual exclusion lock because I think running a few of these
    # commands simultaneously might have been causing issues.
    lock = FileLock('tv_lock.lock', timeout=5)

    
    # Mutual exclusion (danger) zone
    try:
        lock.acquire(timeout=120)
    except Timeout:
        logger.critical('Could not acquire lock within 120 seconds. Something else must have failed catastrophically.')
        exit(1)

    # Wait until HDMI input is detected
    if not wait_hdmi_input(env, 40):
        lock.release()
        logger.error("No HDMI input detected within timeout. Rebooting.")
        reboot(1)
        exit(1)

    # Register the TV, then enable HDMI out, then wake the TV up
    logger.debug('Registering TV...')
    if not register_tv(env):
        lock.release()
        logger.error("Failed to register TV. Rebooting.")
        reboot(1)
        exit(1)

    logger.debug('Enabling HDMI output')
    if not enable_hdmi_out(env):
        lock.release()
        logger.error("Failed to enable HDMI output. Rebooting.")
        reboot(1)
        exit(1)

    logger.debug('Turning on TV')
    if not power_on_tv(env):
        lock.release()
        logger.error("Failed to turn on TV. Rebooting.")
        reboot(1)
        exit(1)

    # Check to make sure the TV is actually on
    logger.debug('Verifying TV is on...')
    if not test_tv_on(env, 10):
        lock.release()
        logger.error("TV did not turn on. Rebooting.")
        reboot(1)
        exit(1)

    # End danger zone
    lock.release()
    
    logger.debug("Display output turned on successfully.")
    logger.debug("Correcting resolution...")
    correct_resolution()

if __name__ == "__main__":
    turn_on()
