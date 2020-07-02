import numpy as np

class ThermalData():
        
    def __init__(self, x, dt):
        
        self.x = x
        self.dt = dt
    
    def _find_nearest(self, array, value):
        
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        
        return array[idx], idx
    
    def get_life(self, C, k, method = None, f = None, location = None, f_span = None):
        
        if method == None:
            method = 'TovoBenasciutti'
            
        if f_span == 0:
            raise ValueError('Frequency span around natural frequency must not be zero: set it to "None" or to a float value.')
            
        if method not in ['Modal', 'TovoBenasciutti', 'Dirlik', 'Rainflow']:
            raise ValueError('Method must be one of: Modal, TovoBenasciutti, Dirlik, Rainflow')
        
        N = self.x.shape[0]
        dt = 1 / fs
        ds = self.x - self.x[0,:,:]
        
        if location is not None:
            (x, y, w, h) = location    
            ds = ds[:, y:(y+h), x:(x+w)]
        
        life = np.zeros(shape=(ds.shape[1], ds.shape[2]))
        npixels = ds.shape[1] * ds.shape[2]  
        
        if method == 'Modal':
            
            if f == None:
                raise ValueError('Natural frequency must be defined')
                
            with tqdm(total = npixels) as pbar:   
                for i in range(ds.shape[1]):
                    for j in range(ds.shape[2]):    
                        
                        fft  = np.abs(np.fft.rfft(ds[:,i,j], N) * 2 / N)
                        freq = np.fft.rfftfreq(N, 1/fs)
            
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
            
            with tqdm(total = npixels) as pbar:
                for i in range(ds.shape[1]):
                    for j in range(ds.shape[2]):
                        
                        tb = FLife.TovoBenasciutti(FLife.SpectralData(ds[:,i,j], self.dt))
                        life[i,j] = tb.get_life(C = C, k = k, method = "method 2")
                        pbar.update(1)
                    
        elif method == 'Dirlik':
            
            with tqdm(total = npixels) as pbar:
                for i in range(ds.shape[1]):
                    for j in range(ds.shape[2]):
                        
                        dirlik = FLife.Dirlik(FLife.SpectralData(ds[:,i,j], self.dt))
                        life[i,j] = dirlik.get_life(C = C, k = k)
                        pbar.update(1)
                    
        elif method == 'Rainflow':
            
            with tqdm(total = npixels) as pbar:    
                for i in range(ds.shape[1]):
                    for j in range(ds.shape[2]):
                        
                        rf = FLife.Rainflow(FLife.SpectralData(ds[:,i,j], self.dt))
                        life[i,j] = rf.get_life(C = C, k = k)
                        pbar.update(1)

        if location is not None:
            return np.mean(life, axis = (0,1))
        else:
            return life