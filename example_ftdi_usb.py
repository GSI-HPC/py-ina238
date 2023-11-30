# SPDX-FileCopyrightText: 2023 GSI Helmholtzzentrum fuer Schwerionenforschung GmbH, Darmstadt, Germany
#
# SPDX-License-Identifier: LGPL-3.0-only

import ti.ina238
import pyftdi.i2c  # pip install pyftdi

bus = pyftdi.i2c.I2cController()
bus.configure("ftdi://ftdi:232h:1/1")  # run `i2cscan.py` to discover url
slave = bus.get_port(0x40)  # i2c address of the TI device to control
pm = ti.ina238.Driver(i2c_slave_port=slave)

print(pm.get_config())
pm.reset()
print(pm.get_config())
pm.set_config(adc_range=ti.ina238.ADCRange.LOW)
print(pm.get_config())
pm.set_config(initial_convdly=42)
print(pm.get_config())
pm.reset()
print(pm.get_config())
pm.set_config(adc_range=ti.ina238.ADCRange.LOW, initial_convdly=42)

print(pm.get_adc_config())
pm.set_adc_config(mode=ti.ina238.Mode.CONTINUOUS_VBUS_VSHUNT_DIETEMP,
                  vbus=ti.ina238.ConversionTime.T_4120_US,
                  vshunt=ti.ina238.ConversionTime.T_4120_US,
                  dietemp=ti.ina238.ConversionTime.T_4120_US,
                  avg_count=ti.ina238.Samples.AVG_256)
print(pm.get_adc_config())

print(pm.get_shunt_calibration())
pm.set_shunt_calibration(r_shunt_ohm=0.04, max_expected_current_ampere=2.5)
print(pm.get_shunt_calibration())
print(pm.get_shunt_voltage())
print(pm.get_bus_voltage())
print(pm.get_current())
print(pm.get_power())
