import numpy as np

class PiersonMoskowitzSpec:

    def __init__(self, U19):
        g = 9.81

        self.U19 = U19
        
        om0 = g / self.U19
        self.k0 = om0**2 / g

        self.Nk = 100
        self.k = np.logspace(-2,1,self.Nk)


    def E_k(self):
        alpha = 8.1e-3
        beta = 0.74

        Ek = alpha / self.k**3 * np.exp(-beta * (self.k0 / self.k)**2)
        return Ek