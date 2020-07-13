import numpy as np
import matplotlib.pyplot as plt 
from tqdm import tqdm
import FLife

class ThermalData():

    """ 
    Termoelasticity-based fatigue life identification.
    The class takes in input a thermal-stress video and gives in output the fatigue life, estimated via modal damage identification [1]
    and standard frequency- and time-domain methods [2]. The natural frequencies to be used in modal damage identification
    approach [1] can be also obtained through frequency analysis.

    [1] Capponi, L., Slavič, J., Rossi, G., Boltežar, M.
        Thermoelasticity-based modal damage identification.
        International Journal of Fatigue, 105661 (2020).
    [2] Slavič J., Mršnik M., Česnik M., Javh J., Boltežar M.. 
        Vibration Fatigue by Spectral Methods, From Structural Dynamics to Fatigue Damage – Theory and Experiments.
        ISBN: 9780128221907, Elsevier, 1st September 2020
     """ 

    def __init__(self, x, dt, x_coord = None, y_coord = None):

        """ 
        Get needed values

        Parameters
        ----------
        x : array_like
            Thermal video of stress measurement values. Correct shape: [frames, width, height]

        dt : float
            Time between discreete signal values 
        
        Methods
        -------
        ._find_nearest()     : Find nearest element in array
        
        ._pixel_selection()  : Pixel coordinates storage
        
        .loc_selection()     : Takes pixel coordinates and defines a roi_size location for the natural frequency identification
        
        .nf_identification() : Natural frequency identification

        .get_life()          : Get the fatigue life

        Raises
        ------
        ValueError : Frequency span around natural frequency must not be zero: set it to 'None' or to a float value.
        ValueError : Method must be one of: Modal, TovoBenasciutti, Dirlik, Rainflow
        """
        
        self.x = x
        self.dt = dt
        self.x_coord = x_coord
        self.y_coord = y_coord

        self.N = self.x.shape[0]
        self.ds = self.x - self.x[0,:,:]
    
    def _find_nearest(self, array, value):

        """
        Find nearest value and its index in array

        Parameters
        ----------
        array : array_like
                Array in which to find the searched value

        value : float
                Searched value

        Return
        ------
        array[idx] : float
                     Nearest value in array

        idx        : int
                     Index of nearest value

        """
        
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        
        return array[idx], idx

    def _pixel_selection(self, event):

        """
        Activate click mouse selection for ROI central pixel

        Return
        ------
        x_coord : float
                  x coordinate of selected pixel
        
        y_coord : float
                  y coordinate of selected pixel

        """

        self.x_coord, self.y_coord = event.xdata, event.ydata
        plt.close()

        return self.x_coord, self.y_coord
    
    def loc_selection(self):

        """
        Plot figure for click mouse selection

        """

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(self.x[0,:,:])
        fig.canvas.mpl_connect('button_press_event', self._pixel_selection)
        plt.show()
            
    def nf_identification(self, location = None, roi_size = None, band_pass = None):

        """
        Natural frequency identification through Fourier analysis applie to the thermal video.

        Parameters
        ----------
        location  : int, optional
                    List of ROI components (x, y, w, h): where x and y are the upper left point coordinates of the ROI,
                    and w and h are the width and the height of the ROI, respectively. If 'None', mouse selection of
                    central point of the ROI is activated. Default to 'None'.

        roi_size  : int, optional
                    Size of the ROI for the natural frequency identification.
                    If 'None', 5 pixel squared ROI size is used. Default to 'None'.

        band_pass : float, optional
                    List of band pass filter frequencies for the natural frequency identification.
                    If 'None', band_pass = [5, 100] [Hz]. Default to 'None'.

        Return
        ------
        nf        : float,
                    Natural frequency identified from thermal video in the selected roi_size location
        """

        if roi_size == None:
            roi_size = 5

        if band_pass == None:
            band_pass = [5, 100]

        if location is not None:
            (x, y, w, h) = location
        else:
            (x, y, w, h) = (int(int(self.x_coord) - (roi_size-1)/2), int(int(self.y_coord) - (roi_size-1)/2), roi_size, roi_size)
            
        self.ds = self.ds[:, y:(y+h), x:(x+w)]

        fft = np.abs(np.fft.rfft(self.ds, self.N, axis = 0) * 2 / self.N)
        freq = np.fft.rfftfreq(self.N, self.dt)

        ampl_nf = np.max(fft[(freq > band_pass[0]) & (freq < band_pass[1])])
        nf = freq[np.where(fft == ampl_nf)[0][0]]

        return np.round(nf, 2)    

    def get_life(self, C, k, method = None, f = None, location = None, f_span = None):

        """
        Fatigue life estimation via modal damage identification and via standard frequency and time-domain methods.
        The frequency and time related methods are based on FLife package.

        Parameters
        ----------
        C           : float
                      Fatigue strength coefficient [MPa**k]

        k           : float
                      Fatigue strength exponent [/].

        method      : string, optional
                      Method to use for the fatigue life estimation.
                      Method = ['Modal', 'TovoBenasciutti', 'Dirlik', 'Rainflow']. If 'None', Tovo Benasciutti's
                      method is used. Default to 'None'. 

        f           : float, optional
                      Natural frequency [Hz]. Necessary if method is 'Modal', otherwise is optional. 

        location    : int, optional
                      List of ROI components (x, y, w, h): x and y are the upper left coordinates of the ROI,
                      and w and h are the width and the height of the ROI, respectively. If 'None', fatigue life is estimated 
                      for the entire spatial domain, otherwise maximum value in the ROI location is given. Default to 'None'.

        f_span      : float, optional
                      Frequency span around the natural frequency where to find the maximum value for the fatigue life estimation.
                      If is 'None', the f_span is 0.1 [Hz].

        Return
        ------
        life        : float
                      Fatigue life [s]

        """

        self.N = self.x.shape[0]
        self.ds = self.x - self.x[0,:,:]


        if f_span == None:
            f_span = 0.1

        if method == None:
            method = 'TovoBenasciutti'

        if f_span == 0:
            raise ValueError('Frequency span around natural frequency must not be zero: set it to "None" or to a float nonzero value.')

        if method not in ['Modal', 'TovoBenasciutti', 'Dirlik', 'Rainflow']:
            raise ValueError('Method must be one of: Modal, TovoBenasciutti, Dirlik, Rainflow')

        if location is not None:
            (x, y, w, h) = location    
            self.ds = self.ds[:, y:(y+h), x:(x+w)]

        life = np.zeros(shape=(self.ds.shape[1], self.ds.shape[2]))
        npixels = self.ds.shape[1] * self.ds.shape[2]  

        with tqdm(total = npixels) as pbar:   
                for i in range(self.ds.shape[1]):
                    for j in range(self.ds.shape[2]):        

                        if method == 'Modal':

                            if f == None:
                                raise ValueError('Natural frequency must be defined')

                            fft  = np.abs(np.fft.rfft(self.ds[:,i,j], self.N) * 2 / self.N)
                            freq = np.fft.rfftfreq(self.N, self.dt)

                            if f_span is not None:
                                x_peak = freq[(freq >= f - f_span) & (freq <= f + f_span)]
                                y_peak = fft[(freq >= f - f_span) & (freq <= f + f_span)]
                                damage = np.sum(x_peak / (C / y_peak**k))

                            else:
                                x_peak = self._find_nearest(freq, f)[0]    
                                y_peak = fft[self._find_nearest(freq, f)[1]]    
                                damage = x_peak / (C / y_peak**k)

                            life[i,j] = 1 / damage
                            pbar.update(1)

                        elif method == 'TovoBenasciutti':

                            tb = FLife.TovoBenasciutti(FLife.SpectralData(self.ds[:,i,j], self.dt))
                            life[i,j] = tb.get_life(C = C, k = k, method = "method 2")
                            pbar.update(1)

                        elif method == 'Dirlik':

                            dirlik = FLife.Dirlik(FLife.SpectralData(self.ds[:,i,j], self.dt))
                            life[i,j] = dirlik.get_life(C = C, k = k)
                            pbar.update(1)

                        elif method == 'Rainflow':

                            rf = FLife.Rainflow(FLife.SpectralData(self.ds[:,i,j], self.dt))
                            life[i,j] = rf.get_life(C = C, k = k)
                            pbar.update(1)

        if location is not None:
            return np.mean(life, axis = (0,1))
        else:
            return life