import numpy as np
import pandas as pd

g = 9.81

class LidarData:
    """
    Extract parameters from the data files to make them accessible
    and calculate the parameterization inputs (match kp, total energy).
    """

    def __init__(self, datafile, label, fetch=False, hogan=False):

        if 'csv' in datafile:
            self.data = pd.read_csv(datafile, header=None, names=['k','Phi'])
        elif 'pkl' in datafile:
            self.data = pd.read_pickle(datafile)
        else:
            raise KeyError('unknown data type')
        
        self.label = label

        self.Hs = self._calc_Hs()
        self.kp = self.data.iloc[self.data['Phi'].idxmax()]['k']

        self.ustar = self.data['ustar'].values[0]
        # * information specific to GOTEX experiment
        if fetch:
            self.Xe = self.data['Xe'].values[0]
            self.U10e = self.data['U10'].values[0]
        # * information specific to ASIT TKE experiment
        if hogan:
            self.u10 = self.data['U10'].values[0]
            self.index = self.data['index'].values[0]
            self.wdir = self.data['Wdir'].values[0]
            
        if 'kn' in self.data.columns:
            self.kn = self.data['kn'].values[0]
        else:
            self.kn = 1e8


    def _calc_Hs(self):
        Hs = 4 * np.sqrt(np.trapz(self.data['Phi'], x=self.data['k']))
        return Hs
    

    def jonswap_inputs(self): 
        X = 22**6 * 16 * 1.6e-7 / self.kp**3 / self.Hs**2
        U10 = np.sqrt(g) / 16 / 1.6e-7 / 22**3 * self.Hs**2 * self.kp**(3/2)
        return X, U10
    

    def pm_inputs(self):
        U19 = np.sqrt(self.Hs / 2.14e-2)
        return U19
    

    def k_to_omega(self):
        self.data['om'] = np.sqrt(g * self.data['k'])
        self.data['Phi_om'] = self.data['Phi'] * 2 * self.data['om'] / g

