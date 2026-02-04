import json
import subprocess
from get_logger import get_logger

logger = get_logger(__name__)

"""
It is expected that the processes calling these functions will handle locking
and mutual exclusion as needed.
"""

def enable_hdmi_out(env: dict) -> bool:
    # Enable HDMI output

    # Equivalent of running `wlopm --on "HDMI-A-1"`
    result = subprocess.run(['/usr/bin/wlopm', '--on', 'HDMI-A-1'], capture_output=True, text=True, env=env)

    # The stupid command returns 0 even on failure, so we have to check stderr.

    # Basic error I get is "ERROR: Output 'HDMI-A-1' does not exist."
    if 'ERROR' in result.stderr:
        logger.error("Failed to enable HDMI output.")
        logger.error(result.stderr.strip())
        return False
    
    # I suppose also check return code just in case
    if result.returncode != 0:
        logger.error("Failed to enable HDMI output.")
        logger.error(result.stderr.strip())
        return False
    
    return True

def disable_hdmi_out(env: dict) -> bool:
    # Disable HDMI output

    # Equivalent of running `wlopm --off "HDMI-A-1"`
    result = subprocess.run(['/usr/bin/wlopm', '--off', 'HDMI-A-1'], capture_output=True, text=True, env=env)

    # Same stupid scenario as above
    if 'ERROR' in result.stderr:
        logger.error("Failed to disable HDMI output.")
        logger.error(result.stderr.strip())
        return False
    
    if result.returncode != 0:
        logger.error("Failed to disable HDMI output.")
        logger.error(result.stderr.strip())
        return False
    
    return True

def is_hdmi_enabled(env: dict) -> bool:
    # Check if HDMI output is enabled

    # Equivalent of running `wlopm --json` and parsing the output
    process_result = subprocess.run(['/usr/bin/wlopm', '--json'], capture_output=True, text=True, env=env)

    logger.debug("wlopm output for HDMI status check:")
    logger.debug(process_result.stdout.strip())

    if process_result.returncode != 0:
        logger.error("Failed to get HDMI output status.")
        logger.error(process_result.stderr.strip())
        return False
    
    if 'ERROR' in process_result.stderr:
        logger.error("Failed to get HDMI output status.")
        logger.error(process_result.stderr.strip())
        return False

    try:
        result: dict[str, str] = json.loads(process_result.stdout)[0]
    except json.JSONDecodeError:
        logger.error("Failed to parse wlopm output as JSON.")
        return False
    
    # I have to be honest, I don't know what this thing errors if I ask for
    # JSON. That's why I'm logging it ig.

    power_mode = result.get('power_mode', 'unknown')

    if power_mode == 'on':
        return True
    else:
        return False
