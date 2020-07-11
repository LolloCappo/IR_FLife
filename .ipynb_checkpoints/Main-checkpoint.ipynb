{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Thermoelasticity-based fatigue life identification"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Import packages"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import pysfmov as sfmov\n",
    "from ThermalData import *"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Material parameters"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "k = 6.51               # Slope endurance curve\n",
    "B = 800.26             # Endurance curve limit [MPa]\n",
    "C = 7.94 * 10**18      # Fatigue strenght [MPa**k]\n",
    "km = 1.2 * 10**(-8)    # Thermoelastic coefficient [Pa**(-1)]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Input thermal video"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "filename = './data/rec.sfmov'        # Filename of thermal acquisition\n",
    "data = sfmov.get_data(filename)      # Using pysfmov to open it as numpy array [°C]\n",
    "\n",
    "fs = 400                             # Smapling frequency [Hz]\n",
    "dt = 1 / fs                          # Time step [s]\n",
    "\n",
    "stress = 10 * (data / km ) * 10**-6  # Stress [MPa]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Class initialization"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "td = ThermalData(stress, dt)        # Class initialization"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Natural frequency identification from thermal video"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### If the location is picked with the mouse click"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib qt               \n",
    "td.loc_selection()           # Mouse selection of central pixel of the roi"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "f = td.nf_identification()   # Natural frequency identification"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### If the location is settled with roi coordinates"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "band_pass = [5,100]         # Band pass filter applied during the natural frequency identification\n",
    "roi = 5                     # ROI size [pixel]\n",
    "location = (39, 79, 5, 5)   # Location of interest in the field of view [pixel]\n",
    "\n",
    "f = td.nf_identification(location = location, roi = roi, band_pass = band_pass)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Fatigue life estimation"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### If the fatigue life is wanted at a particular location"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "location = (39, 79, 5, 5)   # Location of interest in the field of view [pixel]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|█████████████████████████████████████████| 25/25 [00:00<00:00, 648.63it/s]\n",
      "100%|█████████████████████████████████████████| 25/25 [00:00<00:00, 497.50it/s]\n",
      "100%|█████████████████████████████████████████| 25/25 [00:00<00:00, 631.17it/s]\n",
      "100%|█████████████████████████████████████████| 25/25 [00:00<00:00, 104.62it/s]\n"
     ]
    }
   ],
   "source": [
    "md = td.get_life(C, k, 'Modal', f = f, location = location)\n",
    "tb = td.get_life(C, k, 'TovoBenasciutti', location = location)\n",
    "dk = td.get_life(C, k, 'Dirlik', location = location)\n",
    "rf = td.get_life(C, k, 'Rainflow', location = location)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "          Rainflow: 48047 s\n",
      "            Dirlik: 29390 s\n",
      "  Tovo-Benasciutti: 31080 s\n",
      "             Modal: 4106721118 s\n"
     ]
    }
   ],
   "source": [
    "print(f'          Rainflow: {rf:4.0f} s')\n",
    "print(f'            Dirlik: {dk:4.0f} s')\n",
    "print(f'  Tovo-Benasciutti: {tb:4.0f} s')\n",
    "print(f'             Modal: {md:4.0f} s')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### If the fatigue life is wanted even in the spatial domain"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|███████████████████████████████████| 20480/20480 [00:23<00:00, 881.22it/s]\n",
      "100%|███████████████████████████████████| 20480/20480 [00:28<00:00, 713.46it/s]\n",
      "100%|███████████████████████████████████| 20480/20480 [00:28<00:00, 707.73it/s]\n",
      "100%|████████████████████████████████████| 20480/20480 [04:19<00:00, 78.78it/s]\n"
     ]
    }
   ],
   "source": [
    "md = td.get_life(C, k, 'Modal', f = f)\n",
    "tb = td.get_life(C, k, 'TovoBenasciutti')\n",
    "dk = td.get_life(C, k, 'Dirlik')\n",
    "rf = td.get_life(C, k, 'Rainflow')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure()\n",
    "plt.imshow(md)\n",
    "plt.colorbar()\n",
    "plt.clim(1e1,1e14)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
