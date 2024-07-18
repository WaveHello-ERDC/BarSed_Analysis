"""
Class to represent a Run of the wave flume in the BarSed dataset

Author: WaveHello

Date: 07/02/2024
"""
# Standard imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io
from datetime import datetime, timedelta

# Library imports
from lib.data_classes.WaveGauge import WaveGauge
from lib.data_classes.WaveMaker import WaveMaker
from lib.data_classes.ADV import ADV
from lib.general_funcs.datetime_funcs import matlab_datenum_to_datetime
from lib.general_funcs.list_functions import check_val_in_list, apply_mask_2_list
from lib.data_classes.PressureSensor import PressureSensor

class Run:
    # TODO: Update this so that a file directory is based and it does 
    # TODO: Add the pressure gauge data
    # all the rest
    def __init__(self, id, wave_file_path = None, ADV_file_path = None):
        self.id   = id             # Holds the id of the run eg. RUN001
        self.wave_file_path = wave_file_path # Path to the mat file that contains the run's
                                             # wave data
        self.ADV_file_path = ADV_file_path

         # Init variables for later storage
        self.date_time = None
        self.start_date = None
        self.num_times = None
        self.wave_gauges = []      # Variable to hold the wave gauge information
        self.num_wave_gauges = None
        self.wave_maker  = None    # Variable to hold the wave maker information
        
        # Pressure gauge
        self.pressure_gauges = []
        self.num_pressure_gauges = None

        # Init list to hold the ADV objects
        self.ADVs = []
        self.num_ADVs = None

    def __str__(self) -> str:
        """
        Called when the print statement is used on the Run object.
        Returns some metadata about the Run object
        """
        return (f"id: {self.id}\n"
                f"Start Date: {self.start_date}\n"
                f"Wave Data File path: {self.wave_file_path}\n"
                f"Num pressure gagues: {self.num_pressure_gauges}\n"
                f"Num advs: {self.num_ADVs}"
        )
    

    @staticmethod
    def _get_velocity_keys(selected_velocity_keys):
        """
        Check that the input veocity keys are valid and return the keys if the input is valid
        """
        # List of the valid keys
        valid_ADV_keys = ["u_inter", "v_inter", "w_inter", 
                          "u", "v", "w", "u_ens", "v_ens", "w_ens",
                          "u_ens_avg", "v_ens_avg", "w_ens_avg"
        ]
        
        # Check that the input keys are valid
        if selected_velocity_keys == "all":
            # Store all of the keys
            velocity_keys = valid_ADV_keys

        elif selected_velocity_keys is None:
            # Don't load any velocity data
            velocity_keys = []

        else:
            # User selected a subset of the velocity keys

            # Check that the input keys are in the list
            key_valid_list = check_val_in_list(selected_velocity_keys, valid_ADV_keys)

            if not all(key_valid_list):

                # Invert the list so we can get the values that aren't valid
                inverted_valid_list = [not val for val in key_valid_list]

                # Get the values that aren't valid
                invalid_keys = apply_mask_2_list(selected_velocity_keys, inverted_valid_list)

                # If all the keys are valid raise an error
                raise KeyError(f"The following keys: {invalid_keys}/n"
                               f"Are not valid keys the valid keys are: {valid_ADV_keys}"
                               "Or 'all' or None (<- this is the type)"
                               )
            # If all of the keys are valid set the return value
            velocity_keys = selected_velocity_keys
        
        return velocity_keys
    
    def load_wave_data(self):
        """
        Loads the wave data from the mat file and constructs:
            * wave_maker
            * wave_gauges
        """
        # TODO: Move unpacking the data into the wave maker and wave gauge classes

        variable_names = ["date", "eta", "x", "y", "eta_wm", "x_wm"]
        
        # Load the .mat data into a dict
        mat_dict = scipy.io.loadmat(self.wave_file_path, variable_names = variable_names)

        """ Unpack the dict """

        # Get the time
        mat_time = mat_dict["eta"]["date"][0][0][0].flatten()

        # Get the eta
        eta    = mat_dict["eta"]["eta"][0][0]

        # Get the x locations of the wave gauges
        x_loc  = mat_dict["eta"]["x"][0][0].flatten() 

        # Get the y-locations of the wave gauges
        y_loc  = mat_dict["eta"]["y"][0][0].flatten()

        # Get the Surface water elevation in front of the wave maker piston
        eta_wm = mat_dict["eta"]["eta_wm"][0][0].flatten()

        # Get the location of the piston wave maker
        x_wm   = mat_dict["eta"]["x_wm"][0][0].flatten()

        # Convert the time and store it
        self._convert_mat_time_and_store( mat_time)

        # Construct the wave maker
        self._construct_wave_maker(eta_wm, x_wm)

        # Construct the wave gauges
        self._construct_wave_gauges(x_loc, y_loc, eta)

    def load_adv_data(self, selected_velocity_keys = "all"):
        # TODO: make this just adding the adv to the object and move the unpacking into the adv
        """
        Loads the adv data from the ADV mat file.
        Since there is alot of velocity data there's the option to only load some of the keys in the mat file
        """

        # Check that the input keys are valid
        if  not selected_velocity_keys == "all" and \
            not selected_velocity_keys == "None"  and \
            not isinstance(selected_velocity_keys, list):
            
            # Check that the input velocities keys is valid
            raise TypeError("Value should be all, None (<- type None) or a ist of valid keys")

        # Load the file, need this either way
        mat_dict = scipy.io.loadmat(self.ADV_file_path)

        # Open the mat dict and get to the velocity data
        mat_dict = mat_dict["adv"]

        # Store the input wave period
        self.wave_period = mat_dict["per"][0][0][0][0]

        # Store the input wave height
        self.height = mat_dict["H"][0][0][0][0]          

        # Get the datetime and convert it to python datetime
        date_time = matlab_datenum_to_datetime(mat_dict["date_matlab"][0][0].flatten())

        # Get the sensor names
        sensor_names = mat_dict["sensor_names"][0][0]

        # Get the sensor ids
        sensor_ids = [i+1 for i in range(len(sensor_names))]
        
        # Get the height of each of the advs relative to the flume
        flume_heights = mat_dict["z"][0][0].flatten()

        # Get the normalized time
        normalized_time = mat_dict["t_norm"][0][0][0]

        # Get the number of ADVs
        self.num_ADVs = len(sensor_names)
    
        self._construct_ADVs(selected_velocity_keys, sensor_names, sensor_ids, date_time, flume_heights, 
                             normalized_time, mat_dict)

        # Print the number of advs added
        print( f"Added: {self.num_ADVs} ADV(s)" )

    def _construct_ADVs(self, selected_velocity_keys, sensor_names, sensor_ids, date_time, 
                        flume_heights, normalized_time, mat_dict):
        
        # Check that the velocity keys are valid and convert "all" and None 
        # to the proper list
        velocity_keys = self._get_velocity_keys(selected_velocity_keys)
        
        # Loop over all the advs
        for i in range(self.num_ADVs):

            # Get the adv height
            flume_height = flume_heights[i]

            # Get the sensor name
            sensor_name = sensor_names[i]

            # Get the sensor id
            sensor_id = sensor_ids[i]

            # Construct the adv object
            Adv_object = ADV(sensor_name, sensor_id, date_time, flume_height, normalized_time)
            
            # Loop over the velocity keys
            for key in velocity_keys:
                # Load the data from the mat_dict
                velocity_data = mat_dict[key][0][0][i]

                # Store the data in the adv object
                Adv_object.store_velocity_data(key, velocity_data)
            
            # Add the ADV to the list    
            self.ADVs.append(Adv_object)
        
        # Update the number of ADVs
        self.num_ADVs = len(self.ADVs)
    
    def _convert_mat_time_and_store(self, mat_time):
        """
        Convert the time from what it is in the mat file to th matching date time
        """
        experiment_datetime = matlab_datenum_to_datetime(mat_time)

        # Store the full date time array
        self.date_time = experiment_datetime

        # Store the start date
        self.start_date = self.date_time[0].date()

        # Store the number of record times
        self.num_times = len(self.date_time)

    def _construct_wave_maker(self, eta_wm, x_wm):
        """
        Construct the wave maker
        """
        self.wave_maker = WaveMaker(eta_wm, x_wm, self.date_time)
    
    def _construct_wave_gauges(self, x_loc, y_loc, eta):
        """
        Construct the wave gauge objects and store them
        """

        # Init list for temp storage
        wave_gauge_list = []
        # Loop over the locations and construct the wave gauges 
        for id, location in enumerate(zip(x_loc, y_loc)):
    
            # Create the wave gauge
            wave_gauge = WaveGauge(id + 1, location, eta[id], self.date_time)
            
            # Store the wave gauge in the list
            wave_gauge_list.append(wave_gauge)
    
        # Add the wave gauges to the Run object
        self.add_wave_gauge(wave_gauge_list)

    def add_wave_maker(self, wave_maker):
        """
        Add wave maker object to the run
        """

        # Only WaveMaker objects should be passed here
        if isinstance(wave_maker, WaveMaker):
            # Store the WaveMaker in the Run object
            self.wave_maker = wave_maker
        else:
            # Raise an error if the type is wrong
            raise TypeError("Type must be WaveMaker."
                            f" Input type is {type(wave_maker)}")
        
    def add_wave_gauge(self, wave_gauge):
        # Store the wave information inside of the run
        # wave_gauge should be type(WaveGauge) or list

        if isinstance(wave_gauge, list):
            # If multiple wave gauges are being inputted in list concatenate them to the list
            self.wave_gauges = self.wave_gauges + wave_gauge

        elif isinstance(wave_gauge, WaveGauge):
            # if the only one wave gauge is being added just append it to the list
            self.wave_gauges.append(wave_gauge)

        else: 
            raise TypeError("The type must be a list or a WaveGauge object\n"
                            f"Input type is: {type(wave_gauge)}")

        # update the number of wave gauges
        self.num_wave_gauges = len(self.wave_gauges)
        print("New Number of {} wave gauges".format(self.num_wave_gauges))

    def load_pressure_gauge_data(self, pressure_file_path, sites = [2, 4]):
        """
        Load the pressure data, create the pressure gauge objects and store them
        """

        mat_dict = scipy.io.loadmat(pressure_file_path)

        # Get the pressure data
        pressure_data = mat_dict["p0"]

        # Construct and add the pressure gauges
        self._construct_pressure_gauge(pressure_data, sites)

    def _construct_pressure_gauge(self, pressure_data, sites):
        # Loop over the sites and construct the pressure gauge objects
        for i, site_data in enumerate(pressure_data[0, :]):
            # site_data = pressure_data[0, :][0, i]

            # Make the site name
            site_name = f"site_{sites[i]}"

            # Make the pressure object
            pressure_gauge = PressureSensor(id = i+1, location = site_name)

            # Give the pressure gauge the site data and it'll unpack it
            pressure_gauge.store_data(site_data)

            # Add the pressure gauge to the Run object
            self.add_pressure_gauge(pressure_gauge)

    def add_pressure_gauge(self, pressure_gauge):
        """
        Add a pressure gauge to the Run object
        """

        # Add the pressure gauge
        self.pressure_gauges.append(pressure_gauge)

        # update the number of pressure gauges
        self.num_pressure_gauges = len(self.pressure_gauges)

    def construct_wave_gauge_wse(self):
        """
        Construct the water surface elevation (wse) across the entire flume 
        using the wave gauge data
        """

        # Init array to store the surface elevations
        surface_elevations = np.zeros((self.num_times, self.num_wave_gauges))

        # Loop over the wave gauges
        for i, wave_gauge in enumerate(self.wave_gauges):
            # Get the measured water surface
            surface_elevations[:, i] = wave_gauge.eta

        # Store the water surface elevations in the object
        self.wave_gauge_wse = surface_elevations

    def get_wave_gauge_locations(self):
        """
        Get and store the wave gauge locations
        """

        # Number of location dimensions
        num_dim = 2

        # init array to hold the location data
        location = np.zeros((self.num_wave_gauges, num_dim))

        # Set the column indices for where the x and y data should be written
        x_col = 0
        y_col = 1

        # Loop over the wave gauges and store there locations
        for i, wave_gauge in enumerate(self.wave_gauges):
            location[i, x_col] = wave_gauge.location[0]
            location[i, y_col] = wave_gauge.location[1]

        self.wg_locations = pd.DataFrame(location, columns = ["x_loc", "y_loc"])

    def construct_flume_wse(self):
        """
        Construct the wse across the entire flume
        This differs from construct construct_wave_gauge_wse in that it
        includes the surface elevation of the wave maker.
        This adds a little complexity because the location of the wave maker moves
        """
        # Just need to append the wave maker data to the gauge data
        
        x_location = np.zeros((self.num_times, self.num_wave_gauges + 1))
        water_surface_elevation = np.zeros((self.num_times, self.num_wave_gauges + 1))
        
        # Fill the x_location data
        x_location[:, 0]  = self.wave_maker.position

        x_location[:, 1:] = self.wg_locations["x_loc"]

        # Fill the wse data
        water_surface_elevation[:, 0]  = self.wave_maker.eta_wm
        water_surface_elevation[:, 1:] = self.wave_gauge_wse

        # Store the data in the object
        self.flume_wse = water_surface_elevation
        self.flume_wse_locs  = x_location

    def quick_flume_wse_plot(self, time_index, figsize = (8, 4), 
                             legend = False, **kwargs):
        """
        Plot the water surface elevation using the wave gauge data using a 
        """

        #Create the figure plot object
        fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)

        # If multiple times are inputted
        if isinstance(time_index, list):

            # Loop over the time indices ...
            for index in time_index:

                # Store the water surface elevation (wse) and the location
                wse = self.flume_wse[index, :]
                # Only the first location changes because the wave maker moves
                location = self.flume_wse_locs[index, :]

                # Construct the label for the data
                time_label = f"time: {self.date_time[index].time()}"
                
                # Plot the data
                axs.plot(location, wse, label = time_label, **kwargs)

        else:
            #Store the water surface elevation and the location of the measurements (x -direction)
            wse = self.flume_wse[time_index, :]
            location = self.flume_wse_locs[time_index, :]

            # Cosntruct the time label
            time_label = f"time: {self.date_time[time_index].time()}"

            # Plot the data
            axs.plot(location, wse, label = time_label, **kwargs)
        
        # Format the plot
        axs.set_xlabel("Cross-shore distance (m)")
        axs.set_ylabel("Water Surf. Elev. (m)")

        if legend:
            axs.legend()

    def quick_plot_wave_gauges(self, gauge_ids, figsize = (8, 6), 
                               legend = False, ylabel = True,
                               xlabel= True, time_units= "min", **kwargs):
        """
        Plot wave gauge data as a function of time
        """

        if isinstance(gauge_ids, list):
            num_gauges = len(gauge_ids)
        else:
            num_gauges = 1
            # Make the single value into list to make plotting easier
            gauge_ids = [gauge_ids]

        fig, axs = plt.subplots(nrows = num_gauges, ncols = 1, figsize= figsize)

        # Make sure the axs can be looped over even when there's only one plot being created
        axs = np.atleast_1d(axs)

        time= self.date_time

        # Loop over the ids
        for i, id in enumerate(gauge_ids):

            #TODO: Assumes that the wave gauges are in order
            # Which for the time being I'm going to live with
            # Have to shift the id value to match zero indexing
            wave_gauge = self.wave_gauges[id - 1]

            # Select the gauge
            axs[i].plot(time, wave_gauge.eta, label = f"{wave_gauge.id}")

            if ylabel:
                axs[i].set_ylabel("Water Surf. Elev. (m)")
            # Format the xlabel
            if xlabel:
                axs[i].set_xlabel(f"Time {time_units}")
            else:
                axs[i].set_xticklabels([])

            if legend:
                axs[i].legend()