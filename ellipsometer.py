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
        self.wavelength = 632.8

    def getMeasuredPsi(self):
        psi = math.acos((self.voltages[2]-self.voltages[0])/(self.voltages[2]+self.voltages[0]))/2
        return psi

    def getMeasuredDelta(self):
        delta = math.acos((self.voltages[1]-self.voltages[3])/(self.voltages[1]+self.voltages[3])/(math.sin(2*self.getMeasuredPsi())))
        return delta

    def setVoltage(self, measured_voltages):
        self.voltages = measured_voltages


    def getThickness2(self, wavelength, psiMeasured, deltaMeasured):
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

    def getThickness(self):
        thickness = [] # thickness [angstroms]
        deviation = [] # deviation from measured
        devMin = 2000
        d_fit = 0
        psiMeasured = self.getMeasuredPsi()
        deltaMeasured = self.getMeasuredDelta()
        
        for d in range(self.dmin, self.dmax, 20):
            thickness.append(d)

            psiCalc, deltaCalc = Sample.get_psi_delta(d*(10**(-10)), self.wavelength*(10**(-9)))

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
        
