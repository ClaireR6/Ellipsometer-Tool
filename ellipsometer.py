import matplotlib.pyplot as plt
import math
import numpy as np
from sample_model import Sample
from light_sensor import Sensor
from matplotlib.figure import Figure

class Ellipsometer:

    def __init__(self):
        self.intensity = [0,0,0,0]
        self.dmin = 0
        self.dmax = 2000

    def getMeasuredPsi():
        psi = math.acos((self.intensity[2]-self.intensity[0])/(self.intensity[2]+self.intensity[0]))/2
        return psi

    def getMeasuredDelta():
        delta = math.acos((self.intensity[1]-self.intensity[3])/(self.intensity[1]+self.intensity[3])/(math.sin(2*getPsi())))
        return delta

    def setIntensity(index, intensity):
        self.intensity[index] = intensity


    def getThickness(self, wavelength, psiMeasured, deltaMeasured):
        thickness = [] # thickness [angstroms]
        deviation = [] # deviation from measured
        devMin = 2000
        d_fit = 0
        
        for d in range(self.dmin, self.dmax, 20):
            thickness.append(d)

            psiCalc, deltaCalc = Sample.get_psi_delta(d*(10**(-10)), wavelength*(10**(-9)))

            dev = math.sqrt((psiMeasured-psiCalc)**2+(deltaMeasured-deltaCalc)**2)

            if dev<devMin:
                devMin = dev
                d_fit = d
            deviation.append(dev)

        fig = Figure(figsize=(5, 4), dpi=80)
        plot = fig.add_subplot(111)

        plot.scatter(np.array(thickness), np.array(deviation), color='blue')

        plot.set_xlabel('Thickness [Angstroms]')
        plot.set_ylabel('Deviation from Measured Psi and Delta')
        plot.set_title('Deviation Measured vs Thickness')
        return d_fit, fig

    def getThickness(self, wavelength):
        thickness = [] # thickness [angstroms]
        deviation = [] # deviation from measured
        devMin = 2000
        d_fit = 0
        psiMeasured = self.getMeasuredPsi()
        deltaMeasured = self.getMeasuredDelta()
        
        for d in range(self.dmin, self.dmax, 20):
            thickness.append(d)

            psiCalc, deltaCalc = Sample.get_psi_delta(d*(10**(-10)), wavelength*(10**(-9)))

            dev = math.sqrt((psiMeasured-psiCalc)**2+(deltaMeasured-deltaCalc)**2)

            if dev<devMin:
                devMin = dev
                d_fit = d
            deviation.append(dev)

        fig = Figure(figsize=(5, 4), dpi=80)
        plot = fig.add_subplot(111)

        plot.scatter(np.array(thickness), np.array(deviation), color='blue')

        plot.set_xlabel('Thickness [Angstroms]')
        plot.set_ylabel('Deviation from Measured Psi and Delta')
        plot.set_title('Deviation Measured vs Thickness')
        return d_fit, fig
        
