#!/usr/bin/env python3

from wlr_randr_commands import wait_hdmi_input
from cec_ctl_commands import register_tv, power_on_tv, test_tv_on
from wlopm_commands import enable_hdmi_out
from get_env import get_environment
from get_logger import get_logger
from sanity_checks import run_sanity_checks
from correct_resolution import correct_resolution
from shut_down import reboot

def turn_on():
    # I may be a little overzealous with rebooting on failure, but I am tired of
    # having to reboot these things manually when they won't start. So tada. I
    # do that here. Dear lord, I hate tvs

    logger = get_logger(__name__)

    # Sanity checks
    if not run_sanity_checks():
        logger.error("Sanity checks failed. Exiting.")
        exit(1)

    env = get_environment()

    # Wait until HDMI input is detected
    if not wait_hdmi_input(env, 40):
        logger.error("No HDMI input detected within timeout. Rebooting.")
        reboot(1)
        exit(1)

    # Register the TV, then enable HDMI out, then wake the TV up
    logger.debug('Registering TV...')
    if not register_tv(env):
        logger.error("Failed to register TV. Rebooting.")
        reboot(1)
        exit(1)

    logger.debug('Enabling HDMI output')
    if not enable_hdmi_out(env):
        logger.error("Failed to enable HDMI output. Rebooting.")
        reboot(1)
        exit(1)

    logger.debug('Turning on TV')
    if not power_on_tv(env):
        logger.error("Failed to turn on TV. Rebooting.")
        reboot(1)
        exit(1)

    # Check to make sure the TV is actually on
    logger.debug('Verifying TV is on...')
    if not test_tv_on(env, 10):
        logger.error("TV did not turn on. Rebooting.")
        reboot(1)
        exit(1)

    logger.debug("Display output turned on successfully.")
    logger.debug("Correcting resolution...")
    correct_resolution()

if __name__ == "__main__":
    turn_on()
