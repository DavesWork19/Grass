
def time_to_int(time_str):
    """
    Convert time string like '9:30p' or '2:15a' to integer (minutes since midnight).
    
    Args:
        time_str: Time string in format like '9:30p', '2:15a', '11:45pm', '3:00am'
    
    Returns:
        int: Minutes since midnight (0-1439)
    """
    # Clean the string and determine AM/PM
    time_str = time_str.lower().strip()
    is_pm = 'p' in time_str
    
    # Remove am/pm indicators
    time_str = time_str.replace('am', '').replace('pm', '').replace('a', '').replace('p', '')
    
    # Split hours and minutes
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0
    
    # Convert to 24-hour format
    if is_pm and hours != 12:
        hours += 12
    elif not is_pm and hours == 12:
        hours = 0
    
    # Convert to minutes since midnight
    return (hours * 60 + minutes) / 10


