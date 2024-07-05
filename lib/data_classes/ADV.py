# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Library imports


class ADV:
    """
    Class to represent an ADV
    """

    def __init__(self, sensor_name, sensor_id, date_time, flume_height, normalized_time):
        # Init variables for later storage
        self.name  = sensor_name
        self.id           = sensor_id
        self.date_time    = date_time
        self.flume_height = flume_height
        self.norm_t       = normalized_time

        # TODO: Might change this into dataframes in the future

        self.vel = {'u_inter': None, 
                    'v_inter': None,
                    'w_inter': None,
                    'u': None,
                    'v': None,
                    'w': None,
                    'u_ens': None,
                    'v_ens': None,
                    'w_ens': None,
                    'u_ens_avg': None,
                    'v_ens_avg': None,
                    'w_ens_avg': None
        }
        # Init list for later storage
        self.inter_vel = {
                            }
        
        self.cleaned_vel = {
        }

        # Ensemble velocity
        self.ens_vel = { 
        }     

        # Ensemble averge velocity
        self.ens_avg_vel = {
        }


    def __str__(self):
        """
        Returns information about the object, print( obj ) is used
        """

        return_string = ( f"Sensor Name: {self.name} \n"
                          f"Sensor id: {self.id}\n"
                          f"Flume Height, z (m): {self.flume_height}"
        )
        
        return return_string

    def store_velocity_data(self, key, velocity_data):
        """
        Store velocity data inside of the ADV object
        """

        # Check if the key contains inter
        if key in self.vel.keys():
            # Store the data under the right key
            self.vel[key] = velocity_data

            #TODO: Add a condtion to split the "ens" data into each ensemble
            # Also store the number of ensembles in the run
        else:
            raise KeyError(f"Key: {key} is not a valid key.\n"
                           "Valid keys are:\n"
                           f"{self.vel.keys()}\n"
                           )    

    def quick_plot(self, keys, figsize = (8, 4), axs = None, legend = False, **kwargs):
        """
        Generate a quick plot for the given keys
        """
        
        if not isinstance(keys, list):
            # Make the keys into a list
            keys = [keys]

        # Get the number of rows to make in the plot
        # This assuming that everything is going to stack on top of each
        # other but that's fine since this is a quick plot function
        nrows = len(keys)

        if axs is None:
            # Create the figure object
            fig, axs = plt.subplots(nrows = nrows, ncols = 1, figsize =figsize)

        # Make sure that axs is at least an array
        axs = np.atleast_1d(axs)

        for i, ax in enumerate(axs.flat):
            # Get the key
            key = keys[i]
            
            # Haven't implemented the regular ensemble velocities yet
            if key in ["u_ens", "v_ens", "w_ens"]:
                print("WARNING: Plotting the ensembled velocities isn't implemented yet")
                
                # Go to the next iteration of the "for" statement
                continue

            # Get the right time label
            if "ens_avg" in key:
                time = self.norm_t
                time_label = "Normalized Time (-)"
            else: 
                time = self.date_time
                time_label = "Time (s)"

            # Plot the data
            ax.plot(time, self.vel[key], label = key, **kwargs)

            # Format the plot
            ax.set_ylabel("Velocity (m/s)")
            ax.set_label(time_label)

            # Check if the legend should be turned on
            if legend:
                ax.legend()

            plt.tight_layout()

        # TODO: Add function to calculate the depth averaged velocity