"""
Helper function converting bytes to integers.
"""

def to_int16(y1, y2):
    """y1 is LSB
       convert two 8 bit bytes to a signed 16-bit integer
    """
    x = y1 | (y2 << 8)
    if x >= 32768:
        x = -(65536 - x)
    return x


def to_uint32(y1, y2, y3, y4):
    """y1 is LSB"""
    x = y1 | (y2 << 8) | (y3 << 16) | (y4 << 24)
    return x
