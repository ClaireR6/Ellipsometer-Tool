from ellipsometer import Ellipsometer
from gui import GUI
from light_sensor import Sensor

class MainController:
    def __init__(self):
        self.ellipsometer = Ellipsometer()
        self.sensor = Sensor()
        self.voltage_measurements = [1,1,1,1]


    def get_voltage(self):
        voltage = self.sensor.getMeasurement()
        if voltage == None:
            return 1
        return voltage

    def cleanup(self):
        self.sensor.stop()

if __name__ == "__main__":
    main = MainController()
    main.ellipsometer.setVoltage(main.voltage_measurements)
    gui = GUI(main)
    gui.run()


    """TODO: Connect inputs to ellipsometer calculations
             Add outputs: measured psi and delta
             Add inputs: substrate and film constants
    """