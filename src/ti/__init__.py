"""`Texas Instruments <https://www.ti.com>`_ devices"""


from dataclasses import dataclass
from typing import Any


BYTE_SIZE: int = 8  #: Bit
BYTE_ORDER: str = "big"  #: `Big-Endian <https://en.wikipedia.org/wiki/Endianness>`_
VERSION: str = "0.0.1"  #: ina238 package version


@dataclass
class Field:
    """A field is a contiguous number of bits at a certain offset within a TI device register"""

    offset: int
    width: int


@dataclass
class Register:
    """Holds address, size, and fields spec of a TI device register"""

    address: int  #: one Byte wide address
    size: int = 16  #: in Bits
    fields: Any = None
