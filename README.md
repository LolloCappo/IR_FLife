# Thermoelasticity-based fatigue life identification

## Import packages

import numpy as np
import matplotlib.pyplot as plt
import pysfmov as sfmov
from ThermalData import *

## Material parameters

k = 6.51               # Slope endurance curve
B = 800.26             # Endurance curve limit [MPa]
C = 7.94 * 10**18      # Fatigue strenght [MPa**k]
km = 1.2 * 10**(-8)    # Thermoelastic coefficient [Pa**(-1)]

## Input thermal video

filename = './data/rec.sfmov'        # Filename of thermal acquisition
data = sfmov.get_data(filename)      # Using pysfmov to open it as numpy array [°C]

fs = 400                             # Smapling frequency [Hz]
dt = 1 / fs                          # Time step [s]

stress = 10 * (data / km ) * 10**-6  # Stress [MPa]

## Class initialization

td = ThermalData(stress, dt)        # Class initialization

### Natural frequency identification from thermal video

#### If the location is picked with the mouse click

%matplotlib qt               
td.loc_selection()           # Mouse selection of central pixel of the roi

f = td.nf_identification()   # Natural frequency identification

#### If the location is settled with roi coordinates

band_pass = [5,100]         # Band pass filter applied during the natural frequency identification
roi = 5                     # ROI size [pixel]
location = (39, 79, 5, 5)   # Location of interest in the field of view [pixel]

f = td.nf_identification(location = location, roi = roi, band_pass = band_pass)

## Fatigue life estimation

#### If the fatigue life is wanted at a particular location

location = (39, 79, 5, 5)   # Location of interest in the field of view [pixel]

md = td.get_life(C, k, 'Modal', f = f, location = location)
tb = td.get_life(C, k, 'TovoBenasciutti', location = location)
dk = td.get_life(C, k, 'Dirlik', location = location)
rf = td.get_life(C, k, 'Rainflow', location = location)

print(f'          Rainflow: {rf:4.0f} s')
print(f'            Dirlik: {dk:4.0f} s')
print(f'  Tovo-Benasciutti: {tb:4.0f} s')
print(f'             Modal: {md:4.0f} s')

#### If the fatigue life is wanted even in the spatial domain

md = td.get_life(C, k, 'Modal', f = f)
tb = td.get_life(C, k, 'TovoBenasciutti')
dk = td.get_life(C, k, 'Dirlik')
rf = td.get_life(C, k, 'Rainflow')

plt.figure()
plt.imshow(m)
plt.colorbar()
#plt.clim(1e1,1e11)


