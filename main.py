from ellipsometer import Ellipsometer
from gui import GUI
from light_sensor import Sensor

class MainController:
    def __init__(self):
        self.ellipsometer = Ellipsometer()
        self.sensor = Sensor()
        self.voltage_measurements = [0,0,0,0]


    def get_voltage(self):
        voltage = self.sensor.getMeasurement()
        if voltage == None:
            return 0
        return voltage

    def cleanup(self):
        self.sensor.stop()

if __name__ == "__main__":
    main = MainController()
    print(main.sensor.getMeasurement())
    gui = GUI(main)
    psi = main.ellipsometer.getMeasuredPsi(voltage_measurements)
    d, plot = main.ellipsometer.getThickness(632.8, 47, 81)
    print(d)
    gui.set_graph(plot)

    gui.run()


    """TODO: Connect inputs to ellipsometer calculations
             Add outputs: measured psi and delta
             Add inputs: substrate and film constants
    """