Thermoelasticity-based fatigue life identification
---------------------------------------------

Obtaining vibration fatigue life form thermal images acquisition.


Import packages
-----------------------

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    import pysfmov as sfmov
    from ThermalData import *


Material Parameters
-----------------------

.. code-block:: python

    k = 6.51               # Slope endurance curve
    B = 800.26             # Endurance curve limit [MPa]
    C = 7.94 * 10**18      # Fatigue strenght [MPa**k]
    km = 1.2 * 10**(-8)    # Thermoelastic coefficient [Pa**(-1)]

Input thermal video
------------------------
    filename = './data/rec.sfmov'        # Filename of thermal acquisition
    data = sfmov.get_data(filename)      # Using pysfmov to open it as numpy array [°C]

    fs = 400                             # Smapling frequency [Hz]
    dt = 1 / fs                          # Time step [s]

    stress = 10 * (data / km ) * 10**-6  # Stress [MPa]
