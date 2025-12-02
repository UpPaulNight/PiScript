#!/usr/bin/env python3

from wlr_randr_commands import set_display_mode, check_receive_hdmi_input, wait_hdmi_input, test_expected_resolution, test_expected_transform
from get_env import get_environment
from config import mode, transform
from get_logger import get_logger
from sanity_checks import run_sanity_checks


def correct_resolution():

    logger = get_logger(__name__)

    # Sanity checks
    if not run_sanity_checks():
        logger.error("Sanity checks failed. Exiting.")
        exit(1)

    env = get_environment()

    # Don't bother applying settings if no HDMI input is detected
    if not check_receive_hdmi_input(env):
        logger.error("No HDMI input detected. Exiting.")
        exit(1)

    if not test_expected_resolution(mode, env):
        logger.debug(f"Setting display mode to {mode} with transform {transform}.")
        if not set_display_mode(mode, transform, env):
            logger.error("Failed to set display mode. Exiting.")
            exit(1)

        if not test_expected_resolution(mode, env):
            logger.error("Resolution did not change to expected mode after setting it. Exiting.")
            exit(1)
    else:
        logger.debug(f"Display is already at the expected resolution: {mode}.")

    if not test_expected_transform(transform, env):
        logger.debug(f"Setting display transform to {transform}.")
        if not set_display_mode(mode, transform, env):
            logger.error("Failed to set display transform. Exiting.")
            exit(1)

        if not test_expected_transform(transform, env):
            logger.error("Transform did not change to expected value after setting it. Exiting.")
            exit(1)
    else:
        logger.debug(f"Display is already at the expected transform: {transform}.")

if __name__ == "__main__":
    correct_resolution()
