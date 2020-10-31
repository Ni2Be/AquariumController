from .Sensors.MCP3008 import MCP3008
from time import sleep
from time import time
from statistics import median

class DensityMonitor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = MCP3008()
        self.voltage = 3.3
        self.temperature = 20

    def startMonitoring(self):
        counter = 0
        samples = [0] * 30
        while True:
            
            messurement = self.adc.read( channel = self.channel )
            messurementVolt =  (messurement * self.voltage) / 1023.0 
            samples[counter] = messurementVolt
            counter += 1

            if counter is 30:
                medVoltage = median(samples)
                compensationCoefficient = 1 + 0.02 * (self.temperature - 25.0)
                compensationVolatge = medVoltage / compensationCoefficient
                tdsValue = (133.42 * compensationVolatge * compensationVolatge * compensationVolatge - 255.86 * compensationVolatge * compensationVolatge  + 857.39 * compensationVolatge) * 0.5
                
                print("TDS: ", tdsValue, "ppm")
                counter = 0

            sleep(0.004)
