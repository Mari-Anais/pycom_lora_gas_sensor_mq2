import machine

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.adc = machine.ADC()

    def open(self):
        pass

    def read(self, pin):
        pin = self.adc.channel(pin=pin)
        value = pin()
        return value

    def close(self):
        pass
