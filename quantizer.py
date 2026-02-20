import numpy as np


class Quantizer:
    def __init__(self, resolution=0.05):
        self.resolution = resolution

    def encode(self, x, y, z):
        xq = np.round(x / self.resolution).astype(np.int32)
        yq = np.round(y / self.resolution).astype(np.int32)
        zq = np.round(z / self.resolution).astype(np.int32)
        return xq, yq, zq

    def decode(self, xq, yq, zq):
        x = xq * self.resolution
        y = yq * self.resolution
        z = zq * self.resolution
        return x, y, z
    
"""
Creates continous meters into a discreet grid as 
    Integers compress better
    Integers are faster
    Fixed precision is controlled
    Storage becomes predictable
"""