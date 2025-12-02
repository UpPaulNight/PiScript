import subprocess
from get_logger import get_logger

logger = get_logger(__name__)

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