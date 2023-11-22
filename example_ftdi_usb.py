from ti.ina238 import INA238
from pyftdi.i2c import I2cController  # pip install pyftdi

bus = I2cController()
bus.configure("ftdi://ftdi:232h:1/1")  # run `i2cscan.py` to discover url
slave = bus.get_port(0x40)  # i2c address
pmd = INA238(i2c_slave_port=slave)

print(pmd.power_limit)
pmd.power_limit = 42
print(pmd.power_limit)
print(pmd.power_limit)
# print(pmd.power_limit)
