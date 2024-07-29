import numpy as np

def moving_average_filter(data, window_size):
    """
    Applies a moving average filter to the input data.

    Parameters:
    - data: The input array of data points (list or numpy array).
    - window_size: The size of the moving window.

    Returns:
    - filtered_data: The filtered data as a numpy array.
    """
    # Convert data to a numpy array if it is not already
    data = np.array(data)
    
    # Ensure the window size is an integer
    window_size = int(window_size)
    
    # Check if window size is greater than 0 and less than or equal to the length of data
    if window_size <= 0 or window_size > len(data):
        raise ValueError("Window size must be greater than 0 and less than or equal to the length of the data.")
    
    # Compute the moving average using np.convolve with 'valid' mode to avoid padding effects
    filtered_data = np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    
    return filtered_data

if __name__ == "__main__":
    pass