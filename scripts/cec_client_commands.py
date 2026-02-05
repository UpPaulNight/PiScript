import subprocess
from get_logger import get_logger

logger = get_logger(__name__)

"""
It is expected that the processes calling these functions will handle locking
and mutual exclusion as needed.
"""

def demand_tv_on_politely(env: dict):

    # I am tired of dealing with this. Run command. If output or fail, ignore.

    # First log a prayer to the Linux god Linus Torvalds
    logger.info('Please Linus, let the TV turn on... I beg you! 🙏')
    logger.info('If you do not, I shall sacrifice a rubber ducky in your honor! 🦆🔥')

    try:
        # Equivalent of running `echo 'on 0' | cec-client -s`
        result = subprocess.run(['cec-client', '-s'], input='on 0\n', text=True, check=True)
        if result.returncode != 0:
            logger.info('Fuck')
            logger.warning("Failed to demand TV on politely.")
        
    except subprocess.CalledProcessError as e:
        logger.info('Linus why')
        logger.warning("Failed to demand TV on politely.")
        logger.warning(e)
