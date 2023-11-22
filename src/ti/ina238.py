"""`TI INA238 85-V, 16-Bit, High-Precision Power Monitor With I2C Interface <https://www.ti.com/product/INA238>`_"""

from collections import namedtuple


class INA238:
    """`TI <https://www.ti.com>`_ `INA238 <https://www.ti.com/product/INA238>`_ Driver

    :datasheet:`7.6.1 INA238 Registers <GUID-25B37629-8261-48D8-BE56-62622C36C345#TITLE-SBOSA20INA229>`
    """

    #: :datasheet:`7.6.1 INA238 Registers <GUID-25B37629-8261-48D8-BE56-62622C36C345#TITLE-SBOSA20INA229>`
    Register = namedtuple("Register", ["address", "size"])

    CONFIG = Register(address=0x0, size=16)
    ADC_CONFIG = Register(address=0x1, size=16)
    SHUNT_CAL = Register(address=0x2, size=16)
    VSHUNT = Register(address=0x4, size=16)
    VBUS = Register(address=0x5, size=16)
    DIETEMP = Register(address=0x6, size=16)
    CURRENT = Register(address=0x7, size=16)
    POWER = Register(address=0x8, size=24)
    DIAG_ALRT = Register(address=0xB, size=16)
    SOVL = Register(address=0xC, size=16)
    SUVL = Register(address=0xD, size=16)
    BOVL = Register(address=0xE, size=16)
    BUVL = Register(address=0xF, size=16)
    TEMP_LIMIT = Register(address=0x10, size=16)
    PWR_LIMIT = Register(address=0x11, size=16)
    MANUFACTURERER_ID = Register(address=0x3E, size=16)
    MANUFACTURERER_ID_VALUE = 0x5449
    DEVICE_ID = Register(address=0x3F, size=16)
    DEVICE_ID_VALUE = 0x2381

    BYTE_SIZE = 8
    BYTE_ORDER = "big" #: `Big-Endian <https://en.wikipedia.org/wiki/Endianness>`_

    def __init__(self, i2c_slave_port):
        if not i2c_slave_port:
            raise RuntimeError("I2C slave port required")
        self._i2c = i2c_slave_port
        self._reg = self.MANUFACTURERER_ID

    def _write_register(self, register: Register, value: int) -> None:
        """Datasheet Figure 7-7"""
        self._i2c.write(
            [register.address]
            + list(
                value.to_bytes(
                    register.size // self.BYTE_SIZE, byteorder=self.BYTE_ORDER
                )
            )
        )

    def _read(self) -> bytearray:
        """Datasheet Figures 7-8"""
        return bytearray(self._i2c.read(readlen=self._reg.size // self.BYTE_SIZE))

    def _set_register_address(self, register: Register) -> None:
        """Datasheet Figures 7-9"""
        self._i2c.write([register.address])
        self._reg = register

    def _read_register(self, register: Register) -> bytearray:
        if self._reg != register:
            self._set_register_address(register)
        return self._read()

    def _int_from_bytes(self, data: bytearray, **kwargs) -> int:
        if not "byteorder" in kwargs:
            kwargs["byteorder"] = self.BYTE_ORDER
        return int.from_bytes(data, **kwargs)

    @property
    def power_limit(self) -> int:
        """Datasheet 7.6.1.15 POL - This limit compares directly against the value from the
        POWER register to determine if an over power conditions exists.
        """
        return self._int_from_bytes(self._read_register(self.PWR_LIMIT), signed=False)

    @power_limit.setter
    def power_limit(self, value: int) -> None:
        """Datasheet 7.6.1.15 POL - Unsigned, positive value only"""
        assert 0 <= value <= 0xFFFF
        self._write_register(self.PWR_LIMIT, value)

    @property
    def manufacturer_id(self) -> str:
        """Datasheet 7.6.1.16 MANFID - Reads back 'Texas Instruments'"""
        id = int.from_bytes(self._read_register(self.MANUFACTURERER_ID))
        assert self.MANUFACTURERER_ID_VALUE == id
        return hex(id)

    @property
    def device_id(self) -> tuple[str, str]:
        """Datasheet 7.6.1.17 (DIEID, REV_ID) - Device id and revision"""
        id = int.from_bytes(self._read_register(self.DEVICE_ID))
        assert self.DEVICE_ID_VALUE == id
        return (hex((id & 0xFFF0) >> 4), hex(id & 0xF))
