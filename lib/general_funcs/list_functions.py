"""
Module contains functions that are helpful when working with lists

Author: WaveHello

Date: 07/05/2024
"""

def check_val_in_list(input_list, base_list):
    # Returns a list the length of input_list that says if that key is 
    # in base_list

    return [val in base_list for val in input_list]
    
def apply_mask_2_list(input_list, logical_list):
    """
    Applies logical list to input list
    """
    # Get the length of each list
    len_logical = len(logical_list)
    len_input_list = len(input_list)
        
    # Check if they are the same length
    if not len_logical == len_input_list:
        # If the lengths aren't the same return an error
        raise IndexError("The length of the mask and the input list is not the same\n"
                         f"The length of the mask is: {len_logical}\n"
                         f"The length of the input list is: {len_input_list}"
                         )
    # Loop over each value in the input list and logical list and check if the logical
    # is True at that location. If True store that value

    masked_data = [val for val, mask in zip(input_list, logical_list) if mask]
        
    # Return the masked list
    return masked_data
