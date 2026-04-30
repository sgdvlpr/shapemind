import jdatetime
from datetime import date, datetime
from shapemind.config import get_config
from datetime import timedelta

def parse_date(date_str: str) -> date:
    """Parse date string from user input.
    Automatically detects format based on user's calendar setting.
    Also auto-detects if user typed Gregorian when Persian is default
    """

    # Handle special keywords
    if date_str.lower() == "today":
        return date.today()
    if date_str.lower() == "tomorrow":
        return date.today() + timedelta(days=1)
    
    # Try Persian first
    try:
        jd = jdatetime.date.fromisoformat(date_str)
        return jd.togregorian()
    except ValueError: # Raises when, say, year is outside of 1-1500
        pass

    # Try Gregorian
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        pass

    # If both fail, show helpful error
    raise ValueError(f"Invalid date: '{date_str}'. Use YYYY-MM-DD (Persian or Gregorian)")

def format_date(d: date) -> str:
    """Format date for display based on user's calendar preference.
    """
    config = get_config()

    if config["calendar"] == "persian":
        jd = jdatetime.date.fromgregorian(date=d)
        return str(jd)
    else:
        return d.isoformat()
    
def get_today_str() -> str:
    """Get today's date in user's preferred calendar format"""
    config = get_config()
    today = date.today()

    if config["calendar"] == "persian":
        jd = jdatetime.date.fromgregorian(date.today)
        return str(jd)
    else:
        return today.isoformat()
