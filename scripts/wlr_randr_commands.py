import subprocess
from get_logger import get_logger

logger = get_logger(__name__)

"""
It is expected that the processes calling these functions will handle locking
and mutual exclusion as needed.
"""

def set_display_mode(mode: str, transform: str, env: dict) -> bool:
    result = subprocess.run(['/usr/bin/wlr-randr', '--output', 'HDMI-A-1', '--mode', mode, '--transform', transform], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error("Failed to set display.")
        logger.error(result.stderr.strip())
        return False
    return True

def check_receive_hdmi_input(env: dict) -> bool:

    # Just run wlr-randr and see if HDMI-A-1 is listed as connected
    result = subprocess.run(['/usr/bin/wlr-randr'], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error("Failed to run wlr-randr to check HDMI input.")
        logger.error(result.stderr.strip())
        return False
    
    output = result.stdout
    for line in output.splitlines():
        if 'HDMI-A-1' in line:
            return True
    
    return False

def wait_hdmi_input(env: dict, timeout: int = 30) -> bool:
    import time

    start_time = time.time()
    count = 0
    while time.time() - start_time < timeout:
        if check_receive_hdmi_input(env):
            logger.debug('HDMI input detected.')
            return True
        if count == 0:
            logger.debug("Waiting for HDMI input...")
        count += 1
        logger.debug('Check failed')
        time.sleep(1)
    
    logger.error("Timeout waiting for HDMI input.")
    return False

def test_expected_resolution(mode: str, env: dict) -> bool:
    # Run wlr-randr and see if the expected mode is listed for HDMI-A-1
    result = subprocess.run(['/usr/bin/wlr-randr'], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error("Failed to run wlr-randr to check resolution.")
        logger.error(result.stderr.strip())
        return False
    
    output = result.stdout

    # If the mode is set to something like 1920x1080@60, it will appear as
    #
    #   `1920x1080 px, 60.000000 Hz (current)`
    #
    # So we need to process both the mode string and the expected output line.

    # Parse mode string
    mode_parts = mode.split('@')

    # Parse the line that is '(current)'
    for line in output.splitlines():
        if '(current)' in line:
            # Should match a custom regex string like "4096x2160 px, 24.0\d+ Hz"
            expected_line = f"{mode_parts[0]} px, {mode_parts[1]}.\\d+ Hz \\(current\\)"
            import re
            if re.search(expected_line, line):
                return True
    return False
    
def test_expected_transform(transform: str, env: dict) -> bool:
    # Run wlr-randr and see if the expected transform is listed for HDMI-A-1
    result = subprocess.run(['/usr/bin/wlr-randr'], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error("Failed to run wlr-randr to check transform.")
        logger.error(result.stderr.strip())
        return False
    
    output = result.stdout

    # Parse the line that is 'Transform'
    for line in output.splitlines():
        if 'Transform:' in line and transform in line:
            return True
    return False
