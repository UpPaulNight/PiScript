import os
from get_logger import get_logger

logger = get_logger(__name__)

def check_config_exists() -> bool:
    # Check to make sure a config.py file exists
    if not os.path.isfile('config.py'):
        logger.error("config.py file not found. Please create one based on config_template.py")
        return False
    return True

def check_required_variables_in_config() -> bool:
    # Check to make sure required variables are in config.py
    import config

    required_vars = ['mode', 'transform']
    missing_vars = []
    
    for var in required_vars:
        if not hasattr(config, var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required variables in config.py: {', '.join(missing_vars)}")
        return False
    
    return True

def check_mode_correct_format() -> bool:
    # Check to make sure the mode variable is in the correct format

    # An example of correct format is '1920x1080@60' so it should be a simple
    # regex check to see if it matches `^\d+x\d+@\d+$`

    import config
    import re

    mode_pattern = re.compile(r'^\d+x\d+@\d+$')
    if not mode_pattern.match(config.mode):
        logger.error(f"Mode '{config.mode}' is not in the correct format. Expected format is 'WIDTHxHEIGHT@REFRESH_RATE', e.g., '1920x1080@60'")
        return False
    return True

def check_transform_valid() -> bool:
    # Check to make sure the transform variable is valid

    import config

    # The only valid options are: normal, 90, 180, 270, flipped, flipped-90, flipped-180, flipped-270
    valid_transforms = ['normal', '90', '180', '270', 'flipped', 'flipped-90', 'flipped-180', 'flipped-270']
    if config.transform not in valid_transforms:
        logger.error(f"Transform '{config.transform}' is not valid. Valid options are: {', '.join(valid_transforms)}")
        return False
    return True

def run_sanity_checks() -> bool:
    checks = [
        (check_config_exists, "Config file existence"),
        (check_required_variables_in_config, "Required variables in config"),
        (check_mode_correct_format, "Mode format"),
        (check_transform_valid, "Transform validity"),
    ]

    all_passed = True
    for check_func, description in checks:
        if not check_func():
            logger.error(f"Sanity check failed: {description}")
            all_passed = False
        else:
            pass
    
    return all_passed
