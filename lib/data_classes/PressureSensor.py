"""
Class to represent the Pressure sensor
"""
# Standard imports
# import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
# TODO: Fill this class with information

from lib.general_funcs.datetime_funcs import matlab_datenum_to_datetime

class PressureSensor:

    def __init__(self, id, location):
        
        # Store the gauge id (This is made up by WaveHello and corresponds 
        # 1: site 2 
        # 2: site 4
        # At this time I'm still not sure if there's two sites or what's going on

        self.id = id

        # Store the site
        self.location = location

    def __str__(self) -> str:
        return_string = (f"Pressure gauge id: {self.id}\n"
        f"Location: {self.location}"
        )
        
        return return_string

    def store_data(self, site_data):
        """
        Unpacks the data from one of the selected site locations from the 
        mat_dict
        """

        # Convert the datetime from matlab format to python format
        self.date_time = matlab_datenum_to_datetime(site_data[0][0])
        
        # Store the pressure data
        self.pressure = site_data[1][0]

        # Store the start and ending indices in the time-verying data corresponding to 
        # zero up-crossings of the free surface
        self.indices_start_end = site_data[2][0][0][0]

        # Store the start and ending datetime in the time varying data corresponding to the zero-upcrossing 
        # of the free surface
        self.date_start_end = list(site_data[2][0][0][1])

        # Convert the date_start_end to python datetime
        self._convert_date_start_end()

        # Measured wave period from the pressure gauge
        self.period_realization = site_data[2][0][0][2][0]

        # Percent error between the applied wave period and the measured wave period
        self.percent_err_period = site_data[2][0][0][3][0]

    def _convert_date_start_end(self):
        """
        Convert the date_start_end array to datetime.
        This is a nested array so it's easier to just convert it here
        """

        # Convert the upcrossing
        self.date_start_end[0] = matlab_datenum_to_datetime(self.date_start_end[0])

        # Convert the end of the upcrossing
        self.date_start_end[1] = matlab_datenum_to_datetime(self.date_start_end[1])

    def get_number_wave_realizations(self):
        """
        Get the number of wave relizations. This is the number of times a wave was generated in a run.
        This can be gotten from the pressure gauges using the number of wave periods recorded.
        """
        num_wave_realizations = len(self.period_realization)

        # Return the number of wave realizations
        return num_wave_realizations
    
    def quick_plot(self, figsize = (8,4), legend = False, ylim= None, **kwargs):
        """
        Quick plot of the wse at this specific gauge
        """

        # Create the figure object
        fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)

        # Create the plot title
        axs.plot(self.date_time, self.pressure, label = f"Location: {self.location}", **kwargs)
        
        # Format the plot
        axs.set_title(f"Pressure (m) vs. Time (min), Gauge id: {self.id}")
        axs.set_xlabel("Time (min)")
        axs.set_ylabel("Pressure (m)")

        if ylim is not None:
            axs.set_ylim(ylim)
        if legend:
            axs.legend()