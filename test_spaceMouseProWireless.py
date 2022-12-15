import array
import sys

import pytest

import spaceMouseProWireless as sm




class TestUsbInterface:
    @staticmethod
    def test_no_device_found_raises_ValueError():
        with pytest.raises(ValueError):
            ct = sm.SpaceMouseProWireless(usb_vendor_id=0, usb_product_id=0)


class TestParamDictionary:
    def test_write_button_sets_true(self):
        msg = array.array('i', [0, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00])
        ct = sm.SpaceMouseProWireless()
        ct._write_button(msg)

        for item in ct.paramKeyList[6:]:
            assert ct.paramDict[item] == True

    def test_write_button_sets_false(self):
        msg = array.array('i', [0, 0, 0, 0, 0, 0, 0])
        cont = sm.SpaceMouseProWireless()
        cont._write_button(msg)

        for item in cont.paramKeyList[6:]:
            assert cont.paramDict[item] == False

    def test_write_joystick_sets_params_to_neg_val(self):
        # x-Axis inverted in device by manufacturer
        msg = array.array('i', [0, 0xA6, 0xFF, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00])
        ct = sm.SpaceMouseProWireless()
        ct._write_joystick(msg)

        for item in ct.paramKeyList[:6]:
            assert ct.paramDict[item] == -90

    def test_write_released_sets_params_to_none(self):
        ct = sm.SpaceMouseProWireless()
        for key in ct.paramKeyList:
            ct.paramDict[key] = 1
        ct._write_released()

        for key in ct.paramKeyList[:6]:
            assert ct.paramDict[key] == None
        for key in ct.paramKeyList[6:]:
            assert ct.paramDict[key] == False

    @staticmethod
    def test_joystick_moved_or_button_pressed_is_spacemouse_released_returns_false():
        msg = array.array('i', [0, 0xA6, 0xFF, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00])
        assert sm.SpaceMouseProWireless._is_spacemouse_released(msg) == False

    @staticmethod
    def test_spacemouse_released_is_spacemouse_released_returns_true():
        msg = array.array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert sm.SpaceMouseProWireless._is_spacemouse_released(msg) == True

#TODO: _get_usb_msg_timeout_to_none(), _find_usb_device(), get_interrupt_msg(),
# Coverage Analysis




if __name__ == '__main__':
    sys.exit(pytest.main())
