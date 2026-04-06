import math
import cmath
import numpy as np

class Sample:

    def __init__(self):
        self.n_2 = 1.46
        self.k_2 = 0
        self.phi1 = 70
        self.calc()

    def set_constants(self, n2, k2):
        self.n_2 = n2
        self.k_2 = k2

    def set_aoi(self, aoi):
        self.phi1 = aoi

    def calc(self):
        n1 = 1
        k1 = 0
        n3 = 3.85
        k3 = -0.02

        N1 = complex(n1,k1)
        self.N2 = complex(self.n_2,self.k_2)
        N3 = complex(n3,k3)
        phai1 = complex(math.radians(self.phi1),0)
        cosPhi1 = cmath.sqrt(1-cmath.sin(phai1)**2)
        self.cosPhi2 = cmath.sqrt(self.N2**2-(N1**2)*cmath.sin(phai1)**2)/self.N2
        cosPhi3 = cmath.sqrt(N3**2-(N1**2)*cmath.sin(phai1)**2)/N3
        self.rp12 = (self.N2*cosPhi1 - N1*self.cosPhi2)/(self.N2*cosPhi1 + N1*self.cosPhi2)
        self.rs12 = (N1*cosPhi1 - self.N2*self.cosPhi2)/(N1*cosPhi1 + self.N2*self.cosPhi2)
        self.rp23 = (N3*self.cosPhi2 - self.N2*cosPhi3)/(N3*self.cosPhi2 + self.N2*cosPhi3)
        self.rs23 = (self.N2*self.cosPhi2 - N3*cosPhi3)/(self.N2*self.cosPhi2 + N3*cosPhi3)

    def get_psi_delta(self, d, wavelength):
        beta = 2*math.pi*d/wavelength*(self.N2*self.cosPhi2)
        Rp = (self.rp12 + self.rp23*cmath.exp(-2j*beta)) / (1 + self.rp12*self.rp23*cmath.exp(-2j*beta))
        Rs = (self.rs12 + self.rs23*cmath.exp(-2j*beta)) / (1 + self.rs12*self.rs23*cmath.exp(-2j*beta))
        rho = Rp / Rs

        AA = 0
        BB = 0

        psiRad = math.atan(abs(rho))
        if psiRad<0:
            AA = 180

        delRad = cmath.phase(rho)
        if AA == 0 and delRad < 0:
            BB = 360

        Psi = math.degrees(psiRad)
        Delta = (math.degrees(delRad)) + AA + BB
        return Psi, Delta


    # play with sensor to determine i/o hookup
    # Workflow: 
    # user inputs  wavelength, min max d, inputs psi and delta, film index of refraction
    # stepper motor hookup for auto synced I(alpha) measurements?
    # sensor gives voltage for alpha

    # graph x is d, y is squared difference