# SPDX-FileCopyrightText: 2023 GSI Helmholtzzentrum fuer Schwerionenforschung GmbH, Darmstadt, Germany
#
# SPDX-License-Identifier: LGPL-3.0-only

"""`TI INA238 85-V, 16-Bit, High-Precision Power Monitor With I2C Interface <https://www.ti.com/product/INA238>`_"""

from enum import Enum, IntEnum, IntFlag
from dataclasses import asdict, dataclass, fields
import ti
from typing import Any

# fmt: off
class Mode(IntEnum):
    """MODE field values in the ADC_CONFIG device register"""

    SHUTDOWN0                      = 0x0
    TRIGGERED_VBUS                 = 0x1
    TRIGGERED_VSHUNT               = 0x2
    TRIGGERED_VBUS_VSHUNT          = 0x3
    TRIGGERED_DIETEMP              = 0x4
    TRIGGERED_VBUS_DIETEMP         = 0x5
    TRIGGERED_VSHUNT_DIETEMP       = 0x6
    TRIGGERED_VBUS_VSHUNT_DIETEMP  = 0x7
    SHUTDOWN8                      = 0x8
    CONTINUOUS_VBUS                = 0x9
    CONTINUOUS_VSHUNT              = 0xA
    CONTINUOUS_VBUS_VSHUNT         = 0xB
    CONTINUOUS_DIETEMP             = 0xC
    CONTINUOUS_VBUS_DIETEMP        = 0xD
    CONTINUOUS_VSHUNT_DIETEMP      = 0xE
    CONTINUOUS_VBUS_VSHUNT_DIETEMP = 0xF


class ConversionTime(IntEnum):
    """Conversion time values in the VBUSCT, VSHCT, and VTCT fields of the ADC_CONFIG device register"""

    T_50_US   = 0x0  #: 50 µs
    T_84_US   = 0x1  #: 84 µs
    T_150_US  = 0x2  #: 150 µs
    T_280_US  = 0x3  #: 280 µs
    T_540_US  = 0x4  #: 540 µs
    T_1052_US = 0x5  #: 1052 µs
    T_2074_US = 0x6  #: 2074 µs
    T_4120_US = 0x7  #: 4120 µs


class Samples(IntEnum):
    """ADC sample averaging count values in the AVG field of the ADC_CONFIG device register"""

    AVG_1    = 0x0  #: 1 sample
    AVG_4    = 0x1  #: 4 samples
    AVG_16   = 0x2  #: 16 samples
    AVG_64   = 0x3  #: 64 samples
    AVG_128  = 0x4  #: 128 samples
    AVG_256  = 0x5  #: 256 samples
    AVG_512  = 0x6  #: 512 samples
    AVG_1024 = 0x7  #: 1024 samples


class ADCRange(Enum):
    """ADCRANGE field values in the CONFIG device register"""

    HIGH = False  #: ±163.84 mV
    LOW  = True   #: ± 40.96 mV


@dataclass
class Config:
    """CONFIG device register fields"""

    initial_convdly: int
    adc_range: ADCRange

    RESET_BIT       = ti.Field(offset=15, width=1)
    INITIAL_CONVDLY = ti.Field(offset=6,  width=8)
    ADC_RANGE       = ti.Field(offset=4,  width=1)
    RESERVED        = 0b1100_0000_0010_1111


@dataclass
class ADCConfig:
    """ADC_CONFIG device register fields"""

    mode: Mode
    vbus: ConversionTime
    vshunt: ConversionTime
    dietemp: ConversionTime
    avg_count: Samples

    MODE      = ti.Field(offset=12, width=4)
    VBUS      = ti.Field(offset=9,  width=3)
    VSHUNT    = ti.Field(offset=6,  width=3)
    DIETEMP   = ti.Field(offset=3,  width=3)
    AVG_COUNT = ti.Field(offset=0,  width=3)


@dataclass
class ShuntCal:
    """SHUNT_CAL device register fields"""

    shunt_cal: int

    SHUNT_CAL = ti.Field(offset=0, width=15)
    RESERVED  = 0b1000_0000_0000_0000


@dataclass
class DieTemp:
    """DIETEMP device register fields"""

    dietemp: int

    DIETEMP = ti.Field(offset=4, width=12)
    RESERVED = 0b0000_0000_0000_1111


class Resolution:
    VSHUNT_LOW: float     =   5.  #: µV
    VSHUNT_HIGH: float    =   1.25  #: µV
    VBUS: float           =   3.125  #: mV
    DIETEMP: int          = 125  #: m°C
    INITIAL_CONVDLY: int  =   2  #: ms


CONFIG            = ti.Register(address=0x0, fields=Config)
ADC_CONFIG        = ti.Register(address=0x1, fields=ADCConfig)
SHUNT_CAL         = ti.Register(address=0x2, fields=ShuntCal)
VSHUNT            = ti.Register(address=0x4)
VBUS              = ti.Register(address=0x5)
DIETEMP           = ti.Register(address=0x6, fields=DieTemp)
CURRENT           = ti.Register(address=0x7)
POWER             = ti.Register(address=0x8, size=24)
DIAG_ALRT         = ti.Register(address=0xB)
SOVL              = ti.Register(address=0xC)
SUVL              = ti.Register(address=0xD)
BOVL              = ti.Register(address=0xE)
BUVL              = ti.Register(address=0xF)
TEMP_LIMIT        = ti.Register(address=0x10)
PWR_LIMIT         = ti.Register(address=0x11)
MANUFACTURERER_ID = ti.Register(address=0x3E)
DEVICE_ID         = ti.Register(address=0x3F)
# fmt: on


class Driver:
    """`TI <https://www.ti.com>`_ `INA238 <https://www.ti.com/product/INA238>`_ Driver

    :datasheet:`Datasheet 7.6.1 INA238 Device Registers <GUID-25B37629-8261-48D8-BE56-62622C36C345#TITLE-SBOSA20INA229>`
    """

    DEVICE_ID = 0x2381

    def __init__(self, i2c_slave_port):
        if not i2c_slave_port:
            raise RuntimeError("I2C slave port required")
        self._i2c = i2c_slave_port
        self._current_lsb = None
        self.set_register_address(VSHUNT)
        self.get_config()
        self.get_adc_config()

    def write_register(self, register: ti.Register, value: int) -> None:
        """:datasheet:`Datasheet 7.5.1.1 Figure 7-7 <GUID-664FB773-438B-4197-AD9C-C336B45EE590#TITLE-SBOSA20T4877401-6>`"""
        self._i2c.write(
            [register.address]
            + list(
                value.to_bytes(register.size // ti.BYTE_SIZE, byteorder=ti.BYTE_ORDER)
            )
        )

    def read(self) -> bytearray:
        """:datasheet:`Datasheet 7.5.1.1 Figure 7-8 <GUID-664FB773-438B-4197-AD9C-C336B45EE590#TITLE-SBOSA20T4877401-6>`"""
        return bytearray(self._i2c.read(readlen=self._reg.size // ti.BYTE_SIZE))

    def set_register_address(self, register: ti.Register) -> None:
        """:datasheet:`Datasheet 7.5.1.1 Figure 7-9 <GUID-664FB773-438B-4197-AD9C-C336B45EE590#TITLE-SBOSA20T4877401-6>`"""
        self._i2c.write([register.address])
        self._reg = register

    def read_register(self, register: ti.Register) -> bytearray:
        """Read content of given register"""
        if self._reg != register:
            self.set_register_address(register)
        return self.read()

    def int_from_bytes(self, data: bytearray, **kwargs) -> int:
        """Convert given bytearray into an int adhering the proper byteorder"""
        if not "byteorder" in kwargs:
            kwargs["byteorder"] = ti.BYTE_ORDER
        return int.from_bytes(data, **kwargs)

    def _decode_field(self, encoded: int, field: ti.Field) -> int:
        """Decode field from raw device register content"""
        return (encoded & ((~(~0 << field.width)) << field.offset)) >> field.offset

    def _encode_field(self, decoded: int, field: ti.Field) -> int:
        """Encode field for storing to device register"""
        return (decoded & (~(~0 << field.width))) << field.offset

    def get_config(self) -> Config:
        """Read the CONFIG device register"""
        f = CONFIG.fields
        raw = self.int_from_bytes(self.read_register(CONFIG))
        assert 0 == raw & f.RESERVED

        delay = self._decode_field(raw, f.INITIAL_CONVDLY) * Resolution.INITIAL_CONVDLY
        adc_range = ADCRange(bool(self._decode_field(raw, f.ADC_RANGE)))

        if ADCRange.HIGH == adc_range:
            self._vshunt_res = Resolution.VSHUNT_LOW
        else:
            self._vshunt_res = Resolution.VSHUNT_HIGH

        self._config = f(initial_convdly=delay, adc_range=adc_range)

        return self._config

    def set_config(self, **kwargs) -> None:
        """Set the CONFIG device register"""
        f = CONFIG.fields
        new = f(**(asdict(self._config) | kwargs))
        if new != self._config:
            self.write_register(
                CONFIG,
                self._encode_field(
                    new.initial_convdly // Resolution.INITIAL_CONVDLY,
                    f.INITIAL_CONVDLY,
                )
                | self._encode_field(int(new.adc_range.value), f.ADC_RANGE),
            )
            self._config = new

    def get_adc_config(self) -> ADCConfig:
        """Datasheet 7.6.1.2 ADC_CONFIG"""
        raw = self.int_from_bytes(self.read_register(ADC_CONFIG))
        f = ADC_CONFIG.fields

        self._adc_config = ADC_CONFIG.fields(
            mode=Mode(self._decode_field(raw, f.MODE)),
            vbus=ConversionTime(self._decode_field(raw, f.VBUS)),
            vshunt=ConversionTime(self._decode_field(raw, f.VSHUNT)),
            dietemp=ConversionTime(self._decode_field(raw, f.DIETEMP)),
            avg_count=Samples(self._decode_field(raw, f.AVG_COUNT)),
        )

        return self._adc_config

    def set_adc_config(self, **kwargs) -> None:
        """Set the ADC_CONFIG device register"""
        f = ADC_CONFIG.fields
        new = f(**(asdict(self._adc_config) | kwargs))
        if new != self._adc_config:
            self.write_register(
                ADC_CONFIG,
                self._encode_field(new.mode, f.MODE)
                | self._encode_field(new.vbus, f.VBUS)
                | self._encode_field(new.vshunt, f.VSHUNT)
                | self._encode_field(new.dietemp, f.DIETEMP)
                | self._encode_field(new.avg_count, f.AVG_COUNT)
            )
            self._adc_config = new

    def get_shunt_calibration(self) -> int:
        """Datasheet 7.6.1.3 SHUNT_CAL"""
        raw = self.int_from_bytes(self.read_register(SHUNT_CAL))
        f = SHUNT_CAL.fields

        return self._decode_field(raw, f.SHUNT_CAL)

    def set_shunt_calibration(self, r_shunt_ohm: float, max_expected_current_ampere: float):
        """Datasheet 7.6.1.3 SHUNT_CAL and 8.2.1 Current and Power Calculations"""
        assert r_shunt_ohm > 0.
        assert max_expected_current_ampere > 0.

        self._current_lsb = max_expected_current_ampere / (2 ** 15)
        shunt_cal = 819.2 * (10 ** 6) * self._current_lsb * r_shunt_ohm
        if self._config.adc_range == ADCRange.LOW:
            shunt_cal = shunt_cal * 4

        self.write_register(SHUNT_CAL, int(shunt_cal))

    def get_die_temperature(self) -> int:
        """Datasheet 7.6.1.6 DIETEMP"""
        raw = self.int_from_bytes(self.read_register(DIETEMP), signed=True)
        f = DIETEMP.fields

        return self._decode_field(raw, f.DIETEMP) * Resolution.DIETEMP

    def get_current(self) -> float:
        """7.6.1.7 Current Result (CURRENT)"""
        assert self._current_lsb != None
        return self.int_from_bytes(self.read_register(CURRENT), signed=True) * self._current_lsb

    def get_power(self) -> int:
        """7.6.1.8 Power Result (POWER)"""
        assert self._current_lsb != None
        return self.int_from_bytes(self.read_register(POWER)) * self._current_lsb * 0.2

    def reset(self) -> None:
        """Reset the device"""
        f = CONFIG.fields
        self.write_register(CONFIG, self._encode_field(0x1, f.RESET_BIT))
        self.get_config()

    def get_shunt_voltage(self) -> int:
        """7.6.1.4 Shunt Voltage Measurement (VSHUNT) - returns µV"""
        return (
            self.int_from_bytes(self.read_register(VSHUNT), signed=True)
            * self._vshunt_res
        )

    def get_bus_voltage(self) -> int:
        """7.6.1.5 Bus Voltage Measurement (VBUS) Register - returns mV"""
        return (
            self.int_from_bytes(self.read_register(VBUS), signed=True) * Resolution.VBUS
        )

    def get_power_limit(self) -> int:
        """Datasheet 7.6.1.15 POL - This limit compares directly against the value from the
        POWER register to determine if an over power conditions exists.
        """
        return self.int_from_bytes(self.read_register(PWR_LIMIT), signed=False)

    def set_power_limit(self, value: int) -> None:
        """Datasheet 7.6.1.15 POL - Unsigned, positive value only"""
        assert 0 <= value <= 0xFFFF
        self.write_register(PWR_LIMIT, value)

    def get_manufacturer_id(self) -> int:
        """Datasheet 7.6.1.16 MANFID - Reads back 'Texas Instruments'"""
        id = int.from_bytes(self.read_register(MANUFACTURERER_ID))
        assert ti.MANUFACTURERER_ID == id
        return id

    def get_device_id(self) -> int:
        """Datasheet 7.6.1.17 (DIEID, REV_ID) - Device id and revision"""
        id = int.from_bytes(self.read_register(DEVICE_ID))
        assert self.DEVICE_ID == id
        return id
