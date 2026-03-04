import math
import cmath
import numpy as np

class Sample:
    n1 = 1
    k1 = 0
    n2 = 1.46
    k2 = 0
    n3 = 3.85
    k3 = -0.02
    phi1 =70

    N1 = complex(n1,k1)
    N2 = complex(n2,k2)
    N3 = complex(n3,k3)
    phai1 = complex(math.radians(phi1),0)
    cosPhi1 = cmath.sqrt(1-cmath.sin(phai1)**2)
    cosPhi2 = cmath.sqrt(N2**2-(N1**2)*cmath.sin(phai1)**2)/N2
    cosPhi3 = cmath.sqrt(N3**2-(N1**2)*cmath.sin(phai1)**2)/N3
    rp12 = (N2*cosPhi1 - N1*cosPhi2)/(N2*cosPhi1 + N1*cosPhi2)
    rs12 = (N1*cosPhi1 - N2*cosPhi2)/(N1*cosPhi1 + N2*cosPhi2)
    rp23 = (N3*cosPhi2 - N2*cosPhi3)/(N3*cosPhi2 + N2*cosPhi3)
    rs23 = (N2*cosPhi2 - N3*cosPhi3)/(N2*cosPhi2 + N3*cosPhi3)

    @staticmethod
    def get_psi_delta(d, wavelength):
        beta = 2*math.pi*d/wavelength*(Sample.N2*Sample.cosPhi2)
        Rp = (Sample.rp12 + Sample.rp23*cmath.exp(-2j*beta)) / (1 + Sample.rp12*Sample.rp23*cmath.exp(-2j*beta))
        Rs = (Sample.rs12 + Sample.rs23*cmath.exp(-2j*beta)) / (1 + Sample.rs12*Sample.rs23*cmath.exp(-2j*beta))
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