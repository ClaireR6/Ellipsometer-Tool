import matplotlib.pyplot as plt
import math
import numpy as np
from sample_model import Sample
from light_sensor import Sensor
from matplotlib.figure import Figure

class Ellipsometer:

    def __init__(self):
        self.voltages = [1,1,1,1]
        self.dmin = 0
        self.dmax = 2000
        self.wavelength = 633 #In nm
        self.Sample = Sample()
    
    def printVals(self):
        print(self.wavelength, self.Sample.phi1, self.Sample.n_2, self.Sample.k_2)

    def setSampleConstants(self, n, k):
        self.Sample.set_constants(n, k)

    def setSampleAoI(self, angle):
        self.Sample.set_aoi(angle)

    def getWavelength(self):
        return self.wavelength

    # Returns Measured Psi in RADIANS
    def getMeasuredPsi(self):
        psi = math.acos((self.voltages[2]-self.voltages[0])/(self.voltages[2]+self.voltages[0]))/2
        return psi

    # Returns Measured Delta in RADIANS
    def getMeasuredDelta(self):
        delta = math.acos((self.voltages[1]-self.voltages[3])/(self.voltages[1]+self.voltages[3])/(math.sin(2*self.getMeasuredPsi())))
        return delta

    def setVoltage(self, measured_voltages):
        self.voltages = measured_voltages

    # Python wont allow overloads :(
    def getThickness2(self, wavelength, psiMeasured, deltaMeasured):
        thickness, deviation, d_fit = self.getFit(psiMeasured, deltaMeasured)

        fig = Figure(figsize=(5, 4), dpi=80)
        plot = fig.add_subplot(111)

        plot.scatter(np.array(thickness), np.array(deviation), color='blue')

        plot.set_xlabel('Thickness [Angstroms]')
        plot.set_ylabel('Deviation from Measured Psi and Delta')
        plot.set_title('Deviation Measured vs Thickness')
        return d_fit, fig

    def getThickness(self):
        # Need to convert to degress as psiCalc and deltaCalc are in degrees
        psiMeasured = math.degrees(self.getMeasuredPsi())
        deltaMeasured = math.degrees(self.getMeasuredDelta())

        
        thickness, deviation, d_fit = self.getFit(psiMeasured, deltaMeasured)

        fig = Figure(figsize=(5, 4), dpi=80)
        plot = fig.add_subplot(111)

        plot.scatter(np.array(thickness), np.array(deviation), color='blue')

        plot.set_xlabel('Thickness [Angstroms]')
        plot.set_ylabel('Deviation from Measured Psi and Delta')
        plot.set_title('Deviation Measured vs Thickness')
        return d_fit, fig
        
    def getFit(self, psiMeasured, deltaMeasured):
        thickness = [] # thickness [angstroms]
        deviation = [] # deviation from measured
        devMin = 2000
        d_fit = 0

        for d in range(self.dmin, self.dmax, 20):
            thickness.append(d)
            psiCalc, deltaCalc = self.Sample.get_psi_delta(d*(10**(-10)), self.wavelength*(10**(-9)))
    
            dev = math.sqrt((psiMeasured-psiCalc)**2+(deltaMeasured-deltaCalc)**2)
            if dev<devMin:
                devMin = dev
                d_fit = d
            deviation.append(dev)

        return thickness, deviation, d_fit