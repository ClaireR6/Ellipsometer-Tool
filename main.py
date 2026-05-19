from ellipsometer import Ellipsometer
from gui import GUI
from light_sensor import Sensor
from TypedUnit import ureg
from PyOptik import MaterialBank
from datetime import datetime, timedelta

class MainController:
    def __init__(self):
        self.ellipsometer = Ellipsometer()
        self.sensor = Sensor()
        self.voltage_measurements = [1,1,1,1]

    # Returns max voltage from 5 second stream of voltage measurements
    def get_v_max(self):
        v_max = 0
        # Get the current time
        now = datetime.now()

        # Add 5 seconds using timedelta
        future_time = now + timedelta(seconds=5)
        while(datetime.now()<future_time):
            voltage = self.sensor.getMeasurement()
            if voltage > v_max:
                v_max = voltage

        if v_max == 0:
            return 1
        
        return v_max

    # Sends constant voltage stream from Sensor
    def get_voltage(self):
        voltage = self.sensor.getMeasurement()
        if voltage == None:
            return 1
        return voltage
    
    def cleanup(self):
        self.sensor.stop()

if __name__ == "__main__":
    main = MainController()
    main.ellipsometer.setVoltage(main.voltage_measurements) # Sets initial voltage measurements to 1 for all angles and generates a starting graph

    gui = GUI(main)
    gui.run()