"""
Functions that help work with datetime information.

Author: WaveHello

Date: 07/03/2024

"""

# Standard imports
from datetime import datetime, timedelta

def matlab_datenum_to_datetime(matlab_datenums):
    """
    Convert an array of MATLAB datenum to Python datetime.
    """
    # MATLAB datenum's epoch starts at year 0000, while Python's datetime starts at year 0001.
    # There is a difference of 366 days because of MATLAB's usage of the year 0000 as a leap year.
    days = matlab_datenums - 365

    # Convert each datenum to a datetime object
    python_datetimes = [datetime.fromordinal(int(day)) + timedelta(days=day%1) - timedelta(days=1) for day in days]
    
    return python_datetimes