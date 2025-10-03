import numpy as np

g = 9.81

class EquilibriumSpec:

    def __init__(self, kp, Hs, kn):
        self.kp = kp
        self.Hs = Hs
        self.kn = kn

        self.Nk = 100
        self.k = np.logspace(-2,1,self.Nk)

        self.cp = np.sqrt(g/self.kp)
        self._calculate_prefactor()


    def _calculate_prefactor(self):
        k_many = np.logspace(np.log10(self.kp)-2, np.log10(self.kp)+3,2000)

        Pmin = 0
        Pmax = 1e3

        self.P = self._bisect(Pmin, Pmax, k_many)


    def _bisect(self, Pa, Pb, k, tol=1e-6):
        count = 0
        while True:
            # * find midpoint
            Pc = (Pa + Pb)/2

            # * check if reached tolerance
            if (self._F(Pc, k)-self._F(Pa, k)) < tol:
                break

            # * bisect again based on which side the root is in
            if np.sign(self._F(Pb, k)) == np.sign(self._F(Pc, k)):
                Pb = Pc
            else:
                Pa = Pc

            count += 1

        print('    solved for P = {:6f} with {:d} iterations'.format(Pc,count))
        return Pc
    

    def _F(self, P, k):
        # * calculate integral of energy minus (4Hs)^2, for use in bisect
        S = self._Ek(P, k)
        F_S = np.trapz(S,x=k) - self.Hs**2 / 16

        return F_S


    def _Ek(self, P, k):
        # * find prefactor that makes equilibrium and saturation threshold continuous
        B = P / np.sqrt(g) * self.kn**(0.5) * np.exp(-1.25*(self.kp/self.kn)**2)

        Ek = np.zeros(len(k))
        for i in range(len(k)):
            if k[i] < self.kn:
                Ek[i] = P / np.sqrt(g)* k[i]**(-2.5) * np.exp(-1.25*(self.kp/k[i])**2)
            else:
                Ek[i] = B * k[i]**(-3)

        return Ek


    def E_k(self):
        return self._Ek(self.P, self.k)
    