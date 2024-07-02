"""
Class to represent a wave gauge

Author: WaveHello

Date: 07/02/2024
"""
# Standard imports
import matplotlib.pyplot as plt

class WaveGauge:
    wave_gauge_type_dict = {
        1: "self_calibrating",
        2: "self_calibrating",
        3: "self_calibrating",
        4: "fixed",
        5: "fixed",
        6: "fixed",
        7: "fixed",
        8: "fixed",
        9: "fixed",
        10: "fixed",
        11: "fixed",
        12: "ultrasonic",
        13: "ultrasonic",
        14: "ultrasonic",
        15: "ultrasonic",
        16: "ultrasonic",
        17: "ultrasonic",
    }
    def __init__(self, gauge_id, location, eta, datetime):
        self.id = gauge_id       # Store the gauge id
        self.location = location # (x, y) location of the gauge
        self.eta = eta           # Measured surface elevation disturbance
        self.datetime = datetime # Store the time
        self._set_wg_type()      # Set the type of the wave gauge using the id
    
    def __str__(self):
        return_string = (f"Wave Gauge Type: {self.type}\n"
        f"Gauge Id: {self.id}\n"
        f"Location: {self.location}")

        # print the string
        return return_string

    def _set_wg_type(self):
        # Set the wave gauge type using the gauge id
        self.type = WaveGauge.wave_gauge_type_dict[self.id]

    def quick_plot(self, figsize = (8,4), legend = False, ylim= None, **kwargs):
        """
        Quick plot of the wse at this specific gauge
        """

        # Create the figure object
        fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)

        # Create the plot title
        axs.plot(self.datetime, self.eta, label = f"Location (x, y): {self.location}", **kwargs)
        
        # Format the plot
        axs.set_title(f"WSE. (m) vs. Time (min), Gauge id: {self.id}")
        axs.set_xlabel("Time (min)")
        axs.set_ylabel("Water Surf. Elev")

        if ylim is not None:
            axs.set_ylim(ylim)
        if legend:
            axs.legend()




