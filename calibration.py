import numpy as np
import matplotlib.pyplot as plt
import pyLIA
import pysfmov as sfmov

class calibration():    
    
    '''
    Thermoelastic coefficient definition for calibration of thermal acquisition.
    
    Coefficients for standard materials are available from literature [1]. 
    This module allows thermoelastic coefficient identification through strain-gaguge calibration, as presented in [2].
    
    Reference:
    ---------
    [1] Kobayashi, A. 
        Handbook of Experimental Mechanics, London: 2nd rev. Edition: Society for Experimental Mechanics (1993)
    [2] Capponi, L., Slavič, J., Rossi, G., & Boltežar, M.
        Thermoelasticity-based modal damage identification.
        International Journal of Fatigue, 105661 (2020).
    '''
    
    def get_strain(eps, configuration = None):
        
        '''
        Calculate strain for the calibration procedure from strain-gauge acquisition
        
        Input:
        -----
        eps : array_like
            Rows: Time series of measurement values [e]
            Columns: Each strain-gague measurement
                
        configuration : {'90', '120'}, optional
            In case of three strain-gauges usage, define the geometry configuration of the rosette.
            90° and 120° are the available angular configurations of the strain-gauge rosette. Default to None for uniaxial strain-gauge.
        
        Return:
        ------
        strain : float
            Strain for the calibration procedure [e]
        
        '''
       
        if len(eps.shape) == 1:
            return np.max(eps)
        
        elif len(eps.shape) > 1:
            
            if eps.shape[0] < eps.shape[1]:
                raise ValueError('Dimensions of input array: rows and columns need to be transposed.')
            
            elif eps.shape[1] == 2:
                return (np.max(eps[:,0]) + np.max(eps[:,1])) / 2
            
            elif eps.shape[1] == 3:
    
                if configuration not in {'90', '120'}:
                    raise ValueError('Configuration must be 90 or 120 degrees.')
                
                if configuration == '90':
                    return np.abs(np.max(eps[:,1]) - (np.max(eps[:,0]) + np.max(eps[:,2])) / 2)
            
                elif configuration == '120':                
                    return np.abs((np.max(eps[:,0]) - np.max(eps[:,2])) / np.sqrt(3))              
    
    def from_material(m):
        
        '''
        Obtain the thermoelastic coefficient from standard materials
        
        Input:
        -----
        m : {'aluminium', 'epoxy', 'glass', 'magnesium', 'steel', titanium'}
            Standard materials
        
        Return:
        ------
        km : float
            Thermoelastic coefficient [Pa^-1]
        
        '''
        
        material = {'steel' : 3.5 * 10**-12,
                    'aluminium' : 8.8 * 10**-12,
                    'titanium' : 3.5 * 10**-12,
                    'epoxy' : 6.2 * 10**-11,
                    'magnesium' : 1.4 * 10**-11,
                    'glass' : 3.85 * 10**-12}
        
        if m not in material:
            raise ValueError('Material not in the database, please select one in: aluminium, epoxy, glass, magnesium, steel, titanium')
        
        return material[m]
    
    def from_strain_gauge(data, fs, fl, E, ni, strain, location):
        
        '''
        Obtain the thermoelastic coefficient through strain-gauge calibration procedure
        
        Input:
        -----
        data : array_like, [frames, height, width] 
            Sequence of thermal images [°C]
        
        fs : float
            Sampling frequency [Hz]
        
        fl : float
            Load frequency of harmonic excitation [Hz]
            
        E : float
            Young Modulus of the material [Pa]
        
        ni : float
            Poisson's ratio
            
        strain : float
            Strain measured using strain-gauges [e]
            
        location : int, (x,y,w,h)
            ROI coordinates of the area where the strain-gauges are bonded 
            
        Return:
        ------
        km : float
            Thermoelastic coefficient [Pa^-1]
        
        '''
        
        (x,y,w,h) = location
        mag, _ = pyLIA.LIA(data,fs,fl)
        mag_avg = np.mean(mag[y:(y+h),x:(x+w)], axis = (0,1))

        return (mag_avg * (1-ni)) / (E * strain)
    