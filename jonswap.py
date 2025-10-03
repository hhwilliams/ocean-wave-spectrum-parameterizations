import numpy as np

class JONSWAPSpec:

    def __init__(self, X, U10):
        self.g = 9.81

        self.X = X
        self.U10 = U10

        self.Nk = 100
        self.k = np.logspace(-2,1,self.Nk)
        self.om = np.sqrt(self.g * self.k)

        # * peak
        self.wp = 22 * (self.g**2 / self.U10 / self.X)**(1/3)
        self.kp = self.wp**2 / self.g

        # * defaults
        self.s = np.array([0.09 if k > self.kp else 0.07 for k in self.k])
        self.r = self._default_r()
        self.gam = 3.3


    def _default_r(self):
        return np.exp(-(np.sqrt(self.k) - np.sqrt(self.kp))**2  / (2*self.s**2 * self.kp))


    def E_k(self):
        gam_r = self.gam**self.r
        alpha = 0.076 * (self.U10**2 / self.g / self.X)**0.22
        Ek = alpha / 2 * self.k**(-3) * np.exp(-1.25 * (self.kp / self.k)**2) * gam_r

        return Ek
    

    # def E_om(self):
    #     Eom = 2 * self.om / self.g * self.E_k()
    #     return Eom
    

    # def set_s(self, s1, s2):
    #     self.s =  np.array([s2 if k > self.kp else s1 for k in self.k])

    # def set_r(self, power, denom):
    #     self.r = np.exp(-(np.sqrt(self.k) - np.sqrt(self.kp))**power  / (denom * self.s**2 * np.sqrt(self.kp)**power))

    # def set_gamma(self, gamma):
    #     self.gam = gamma

