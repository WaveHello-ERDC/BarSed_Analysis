"""
Functions for doing kimematic functions,
acceleration, velocity, displacement, no forces
"""

def calc_velocity(position, time):
    """
    Calc the velocity from a given position time series and time series
    """

    # Calc the incremental displacement
    inc_displacement = position[1:] - position[:-1]

    # Calc the incremental time
    inc_time = time[1:] - time[:-1]

    # Calc the velocity
    velocity = inc_displacement/inc_time

    # return the velocity
    return velocity


if __name__ == "__main__":
    pass