from get_logger import get_logger
import subprocess
from datetime import datetime
import os

logger = get_logger(__name__)

def up_shutdown_counter() -> None:
    # To prevent this from shutting down repeatedly, limit the number of
    # shutdowns to twice a day. Just create a file that contains today's date
    # and the count
    from datetime import datetime
    import os
    counter_file = 'shutdown_counter.txt'
    today_str = datetime.now().strftime('%Y-%m-%d')
    count = 0
    if os.path.exists(counter_file):

        with open(counter_file, 'r') as f:
            line = f.readline().strip()
            
        if line:
            date_str, count_str = line.split(',')
            if date_str == today_str:
                count = int(count_str)
    count += 1
    with open(counter_file, 'w+') as f:
        f.write(f"{today_str},{count}\n")

def can_shutdown() -> bool:
    # Check if we can shut down based on the shutdown counter

    counter_file = 'shutdown_counter.txt'
    today_str = datetime.now().strftime('%Y-%m-%d')

    if not os.path.exists(counter_file):
        return True
    
    with open(counter_file, 'r') as f:
        line = f.readline().strip()
    
    if not line:
        return True
    
    date_str, count_str = line.split(',')
    if date_str == today_str and int(count_str) >= 2:
        logger.debug("Shutdown limit reached for today.")
        return False
    return True
    
def shut_down(minutes_delay: int) -> bool:
    # Schedule a system shutdown after a specified delay in minutes

    if not can_shutdown():
        logger.info("Not scheduling shutdown due to daily limit.")
        return False

    logger.debug(f"Scheduling shutdown in {minutes_delay} minutes.")

    # Equivalent of `sudo shutdown -h +<minutes_delay>`
    result = subprocess.run(['sudo', 'shutdown', f'+{minutes_delay}'], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("Failed to schedule shutdown.")
        logger.error(result.stderr.strip())
        return False
        
    up_shutdown_counter()
    return True

def reboot(minutes_delay: int) -> bool:
    # Schedule a system reboot after a specified delay in minutes

    if not can_shutdown():
        logger.info("Not scheduling shutdown due to daily limit.")
        return False

    logger.debug(f"Scheduling reboot in {minutes_delay} minutes.")

    # Equivalent of `sudo shutdown -r +<minutes_delay>`
    result = subprocess.run(['sudo', 'shutdown', '-r', f'+{minutes_delay}'], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("Failed to schedule reboot.")
        logger.error(result.stderr.strip())
        return False
        
    up_shutdown_counter()
    return True
