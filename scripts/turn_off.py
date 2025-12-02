#!/usr/bin/env python3

from wlr_randr_commands import set_display_mode, wait_hdmi_input
from cec_ctl_commands import power_off_tv, register_tv
from wlopm_commands import disable_hdmi_out
from get_env import get_environment
from get_logger import get_logger
from sanity_checks import run_sanity_checks

def turn_off():

    logger = get_logger(__name__)

    # Sanity checks
    if not run_sanity_checks():
        logger.error("Sanity checks failed. Exiting.")
        exit(1)

    env = get_environment()

    # Wait until HDMI input is detected
    if not wait_hdmi_input(env, 40):
        logger.error("No HDMI input detected within timeout. Exiting.")
        exit(1)

    # Set the resolution to lower. Idk if this actually helps with anything but
    # whatever.
    set_display_mode('720x480@60', 'normal', env)

    # Register the TV, then disable HDMI out, then put the TV in standby mode

    logger.debug('Registering TV...')
    if not register_tv(env):
        logger.error("Failed to register TV. Exiting.")
        exit(1)

    logger.debug('Disabling HDMI output')
    if not disable_hdmi_out(env):
        logger.error("Failed to disable HDMI output. Exiting.")
        exit(1)

    logger.debug('Turning off TV')
    if not power_off_tv(env):
        logger.error("Failed to turn off TV. Exiting.")
        exit(1)

    logger.debug("Display output turned off successfully.")

if __name__ == "__main__":
    turn_off()
