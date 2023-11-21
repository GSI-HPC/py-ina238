"""
For reference: https://github.com/torvalds/linux/blob/master/drivers/hwmon/ina238.c

When connecting to the INA238 IC via I2C over an FT232H USB adapter, the above kernel
driver cannot be used. Instead, we have to fall back to a python implementation of
a I2C-over-USB driver based on [pyftdi](https://github.com/eblot/pyftdi).

Side note: There has been some work published by Mike Krinkin to expose a standard
linux I2C bus via the ftdi_sio kernel driver, but this is not (yet?) upstreamed into
the vanilla linux kernel, see https://krinkinmu.github.io/2020/09/06/ftdi-i2c.html.
"""

import os

os.environ["BLINKA_FT232H"] = "1"

from adafruit_bus_device import i2c_device
import board  # import AFTER setting the env variable
from collections import namedtuple


class INA238:
    """85-V, 16-Bit, High-Precision Power Monitor With I2C Interface (https://www.ti.com/product/INA238)"""

    Register = namedtuple("Register", ["address", "size"])

    # Registers
    _CONFIG = Register(address=0x0, size=16)  # Configuration
    _ADC_CONFIG = Register(address=0x1, size=16)  # ADC Configuration
    _SHUNT_CAL = Register(address=0x2, size=16)  # Shunt Calibration
    _VSHUNT = Register(address=0x4, size=16)  # Shunt Voltage Measurement
    _VBUS = Register(address=0x5, size=16)  # Bus Voltage Measurement
    _DIETEMP = Register(address=0x6, size=16)  # Temperature Measurement
    _CURRENT = Register(address=0x7, size=16)  # Current Result
    _POWER = Register(address=0x8, size=24)  # Power Result
    _DIAG_ALRT = Register(address=0xB, size=16)  # Diagnostic Flags and Alert
    _SOVL = Register(address=0xC, size=16)  # Shunt Overvoltage Threshold
    _SUVL = Register(address=0xD, size=16)  # Shunt Undervoltage Threshold
    _BOVL = Register(address=0xE, size=16)  # Bus Overvoltage Threshold
    _BUVL = Register(address=0xF, size=16)  # Bus Undervoltage Threshold
    _TEMP_LIMIT = Register(address=0x10, size=16)  # Temperature Over-Limit Threshold
    _PWR_LIMIT = Register(address=0x11, size=16)  # Power Over-Limit Threshold
    _MANUFACTURERER_ID = Register(address=0x3E, size=16)  # Manufacturere ID
    _DEVICE_ID = Register(address=0x3F, size=16)  # Device ID

    _I2C_BUS_ADDR = 0x40  # see CurrentMonitor_V0.kicad_sch and Datasheet Table 7-2

    _BYTE_SIZE = 8

    def __init__(self):
        self._i2c = i2c_device.I2CDevice(board.I2C(), self._I2C_BUS_ADDR)

    def _read_register(self, register: Register) -> bytearray:
        """Datasheet Figures 7-9 and 7-8"""
        with self._i2c as i2c:
            i2c.write(bytes([register.address & 0xFF]))
            result = bytearray(register.size // self._BYTE_SIZE)
            i2c.readinto(result)
            return result

    def _write_register(self, register: Register, value: int) -> None:
        """Datasheet Figure 7-7"""
        with self._i2c as i2c:
            i2c.write(bytes([register.address & 0xFF, value & 0xFF]))

    @property
    def power_limit(self) -> int:
        """Datasheet 7.6.1.15 POL - This limit compares directly against the value from the
        POWER register to determine if an over power conditions exists.
        """
        return int.from_bytes(self._read_register(self._PWR_LIMIT))

    @power_limit.setter
    def power_limit(self, value: int) -> None:
        """Datasheet 7.6.1.15 POL - Unsigned, positive value only"""
        assert 0 <= value <= 0xFFFF
        self._write_register(self._PWR_LIMIT, value)

    @property
    def manufacturer_id(self) -> str:
        """Datasheet 7.6.1.16 MANFID - Reads back 'Texas Instruments'"""
        id = int.from_bytes(self._read_register(self._MANUFACTURERER_ID))
        assert 0x5449 == id
        return hex(id)

    @property
    def device_id(self) -> tuple[str, str]:
        """Datasheet 7.6.1.17 (DIEID, REV_ID) - Device id and revision"""
        id = int.from_bytes(self._read_register(self._DEVICE_ID))
        assert 0x2381 == id
        return (hex((id & 0xFFF0) >> 4), hex(id & 0xF))
