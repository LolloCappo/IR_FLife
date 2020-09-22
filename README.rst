Thermoelasticity-based fatigue life estimation
---------------------------------------------

.. image:: https://zenodo.org/badge/274091654.svg
   :target: https://zenodo.org/badge/latestdoi/274091654

Estimation of vibration fatigue life from thermal images acquisition.
The class is based on the modal damage via thermoelasticity [1] and on the FLife package [2].

Install packages using pip
-----------------------

.. code-block:: python

    pip install IR_FLife

Import packages
-----------------------

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    import pysfmov as sfmov
    import IR_FLife as irfl


Material Parameters
-----------------------

.. code-block:: python

    k = 6.51               # Slope endurance curve
    B = 800.26             # Endurance curve limit [MPa]
    C = 7.94 * 10**18      # Fatigue strenght [MPa**k]
    km = 1.2 * 10**(-8)    # Thermoelastic coefficient [Pa**(-1)]

Input thermal video
------------------------

.. code-block:: python

    filename = './data/rec.sfmov'        # Filename of thermal acquisition
    data = sfmov.get_data(filename)      # Using pysfmov to open it as numpy array [°C]

    fs = 400                             # Smapling frequency [Hz]
    dt = 1 / fs                          # Time step [s]

    stress = 10 * (data / km ) * 10**-6  # Stress [MPa]

Class initialization
------------------------

.. code-block:: python

    td =  irfl.IR_FLife(stress, dt)       # Class initialization

Natural frequency identification from thermal video
---------------------------------------------------

If the location is picked with the mouse click

.. code-block:: python
             
    td.loc_selection()           # Mouse selection of central pixel of the roi
    f = td.nf_identification()   # Natural frequency identification

If the location id settled with roi cooirdinates

.. code-block:: python
    
    band_pass = [5,100]         # Band pass filter applied during the natural frequency identification
    roi_size = 5                # ROI size [pixel]
    location = (39, 79, 5, 5)   # Location of interest in the field of view [pixel]

    f = td.nf_identification(location = location, roi_size = roi_size, band_pass = band_pass)

Fatigue life estimation
-----------------------

If the fatigue life is wanted at a particular location

.. code-block:: python

    location = (39, 79, 5, 5)   # Location of interest in the field of view [pixel]

    md = td.get_life(C, k, 'Modal', f = f, location = location)
    tb = td.get_life(C, k, 'TovoBenasciutti', location = location)
    dk = td.get_life(C, k, 'Dirlik', location = location)
    rf = td.get_life(C, k, 'Rainflow', location = location)

    print(f'          Rainflow: {rf:4.0f} s')
    print(f'            Dirlik: {dk:4.0f} s')
    print(f'  Tovo-Benasciutti: {tb:4.0f} s')
    print(f'             Modal: {md:4.0f} s')

If the fatigue life is wanted in the spatial domain

.. code-block:: python

    md = td.get_life(C, k, 'Modal', f = f)
    tb = td.get_life(C, k, 'TovoBenasciutti')
    dk = td.get_life(C, k, 'Dirlik')
    rf = td.get_life(C, k, 'Rainflow')

Then, the spatial domain results are shown:

.. code-block:: python

    plt.figure()

    plt.subplot(2,2,1)
    plt.imshow(dk)
    plt.colorbar()
    plt.title('Dirlik')

    plt.subplot(2,2,2)
    plt.imshow(md)
    plt.colorbar()
    plt.title('Modal approach')

    plt.subplot(2,2,3)
    plt.imshow(rf)
    plt.colorbar()
    plt.title('Rainflow')

    plt.subplot(2,2,4)
    plt.imshow(tb)
    plt.colorbar()
    plt.title('Tovo-Benasciutti')



Reference:

[1] Thermoelasticity-based modal damage identification.
    Lorenzo Capponi, Janko Slavič, Gianluca Rossi, Miha Boltežar
    International Journal of Fatigue (2020)

[2] Vibration Fatigue by Spectral Methods, From Structural Dynamics to Fatigue Damage – Theory and Experiments.
    Janko Slavič, Matjaž Mršnik, Martin Česnik, Jaka Javh, Miha Boltežar.
    ISBN: 9780128221907, Elsevier, 1st September 2020.
