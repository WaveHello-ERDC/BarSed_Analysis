"""
Class to represent the wave maker

Author: WaveHello

Date: 07/02/2024
"""

# Standard imports
import matplotlib.pyplot as plt

# Libary imports

class WaveMaker:
    def __init__(self, eta_wm, position, datetime):
        self.eta_wm = eta_wm         # Store the free surface elevation at the 
                                     # face of the wave maker

        self.position = position     # Cross-position of the face of the piston type wave maker
                                     # relative to its starting position, x = 0
        
        self.datetime  = datetime 
        self.num_times = len(eta_wm) # Number of recorded times

    def __str__(self) -> str:
        """
        Returns information about the WaveMaker object when the print()
        statement is used on the object
        """

        # String of metadata to write 
        return_string = ("Wave Maker information:\n"
                         f"Number of times: {self.num_times}"
        )

        return return_string
    
    def quick_position_plot(self, figsize = (8,4), axs = None, legend = False, **kwargs):
        """
        Plot the location of the wave maker as a function of time
        """

        if axs is None:
            # Create the figure object
            fig, axs = plt.subplots(nrows = 1, ncols =1 , figsize = figsize)

        # Plot the data
        axs.plot(self.datetime, self.position, **kwargs)

        axs.set_title("Wave Maker position vs. Time")
        axs.set_xlabel("Time (min)")
        axs.set_ylabel("x-position(m)")

        if legend:
            axs.legend()

    def quick_wse_plot(self, figsize = (8,4), axs = None, legend = False, **kwargs):
        """
        Plot the water surface elevation infront of the wave maker vs. time
        """

        # If an axis isn't paced make a new one
        if axs is None:
            # Create the figure object
            fig, axs = plt.subplots(nrows = 1, ncols =1 , figsize = figsize)

        # Otherwise used the provided axis

        # Plot the data
        axs.plot(self.datetime, self.eta_wm, **kwargs)

        axs.set_title("Wave Maker WSE vs. Time")
        axs.set_xlabel("Time (min)")
        axs.set_ylabel("Water Surf. Elev. (m)")

        if legend:
            axs.legend()