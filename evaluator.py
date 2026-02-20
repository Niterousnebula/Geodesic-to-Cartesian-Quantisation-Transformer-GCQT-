import numpy as np


def compute_error(original, reconstructed):
    error = np.abs(original - reconstructed)
    return np.mean(error), np.max(error)
"""
This module:
    Compares original ENU
    Compares reconstructed ENU
    Computes mean & max error
"""