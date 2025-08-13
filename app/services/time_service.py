"""
Time Service - Simple functions to get current time and date
This is one of the tools our AI bot can use
"""

from datetime import datetime

def get_current_time(timezone=None):
    """
    Get the current time and date.
    
    Args:
        timezone: Optional timezone (like 'UTC', 'Europe/Tbilisi')
    
    Returns:
        A string with current time and date
    """
    # Get current time
    now = datetime.now()
    
    # Format it nicely
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Add timezone info if provided
    if timezone:
        time_string += f" ({timezone})"
    
    return f"Current time: {time_string}"

def get_current_date():
    """Get just the current date."""
    now = datetime.now()
    date_string = now.strftime("%A, %B %d, %Y")
    return f"Today is: {date_string}"

# Example usage:
# print(get_current_time())  # Output: Current time: 2025-08-11 18:45:30
# print(get_current_date())  # Output: Today is: Monday, August 11, 2025 