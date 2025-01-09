import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy as sc
from scipy.ndimage import gaussian_filter1d
from scipy.stats import binom
from scipy.optimize import bisect

if __name__ == "__main__":
    print("Testing that libraries are working.")
    print("Pandas version: ", pd.__version__)
    print("Numpy version: ", np.__version__)
    print("Matplotlib version: ", matplotlib.__version__)
    print("Scipy version: ", sc.__version__)
    print("Python smoke test finished successfully :)")