import pytest
import sys

from byteToIntConversion import *


class Test2BytesToIntegerConversion:
    @staticmethod
    def test_twos_complement_negative_number_returned_int16():
        res = to_int16(255, 255)
        assert res == -1

    @staticmethod
    def test_zero_returns_zero_int16():
        res = to_int16(0, 0)
        assert res == 0

    @staticmethod
    def test_edge_case_max_number_int16():
        res = to_int16(255, 127)
        assert res == 32767

    @staticmethod
    def test_edge_case_min_number_int16():
        res = to_int16(0, 128)
        assert res == -32768

    @staticmethod
    def test_lsb_first_argument_int16():
        res = to_int16(1, 0)
        assert res == 1


class Test4BytesToUnsignedIntegerConversion:
    @staticmethod
    def test_no_twos_complement_positive_number_returned_uint32():
        res = to_uint32(1, 0, 0, 128)
        assert res == 0x80000001

    @staticmethod
    def test_zero_returns_zero_uint32():
        res = to_uint32(0, 0, 0, 0)
        assert res == 0

    @staticmethod
    def test_edge_case_max_number_uint32():
        res = to_uint32(255, 255, 255, 255)
        assert res == 0xFFFFFFFF

    @staticmethod
    def test_lsb_first_argument_and_correct_order_uint32():
        res = to_uint32(1, 2, 3, 4)
        assert res == 0x4030201


if __name__ == '__main__':
    sys.exit(pytest.main())
