from labquest import LabQuest

lq = LabQuest()

class Sensor:
    def __init__(self):
        lq.open()
        lq.select_sensors(ch1='raw_voltage') 
        lq.start(100)

    def getMeasurement(self):
        ch1_measurement = lq.read('ch1')
        return ch1_measurement

    def stop(self):
        lq.stop()
        lq.close()

    def get_sensor(self):
        return lq.select_sensors(['A'])

    def flush_buffer(self):
        """Reads and discards all data currently in the buffer."""
        # Most LabQuest libraries return an empty list or None 
        # when the buffer is empty.
        data = lq.read('ch1')
        while not (data is None):
            data = lq.read('ch1')

# A very simple iterated reading of 10 measurements in the span of 
''' 
lq.start()
Start collecting data at a specified period (time between samples). 
This function takes an argument to set the period in milliseconds. 
For example, lq.start(1000) to sample every 1000 milliseconds, or lq.start(100) to sample every 100 milliseconds. 
'''