"""
V2: Try to write tests only on public functions, targeting functionality.
-> Otherwise refactoring becomes impossible because every function is fixed.

USB-package is replaced with a stub before this file is loaded, in conftest.py.
This allows for less fixtures and mocking, and also correct handling of (stubbed) usb resource
disposal without headaches.
"""

import pytest
import sys
import array

import spaceMouseProWireless as Sm
import stub_usb.core

# ===================== File-wide Fixtures =================================
@pytest.fixture(scope='function')
def mock_ct():
    ct = Sm.SpaceMouseProWireless()

    return ct


class TestUsbConnectionEstablishment:
    # ===================== Tests ==========================================
    @staticmethod
    def test_no_usb_device_found_raises_value_error(mocker):
        mocker.patch(
            'usb.core.find',
            return_value=None
        )

        with pytest.raises(ValueError):
            ct = Sm.SpaceMouseProWireless()

    @staticmethod
    def test_usb_device_found_reference_object_saved_to_class_attribute__dev(mock_ct):
        msg = stub_usb.core.Device().msg
        assert mock_ct._dev.msg == msg

    @staticmethod
    def test_usb_is_kernel_driver_active_is_verified(mocker):
        mocker.patch.object(
            stub_usb.core.Device,
            'is_kernel_driver_active'
        )

        ct = Sm.SpaceMouseProWireless()
        ct._dev.is_kernel_driver_active.assert_called_once()

    @staticmethod
    def test_usb_detach_kernel_driver_fails_raises_runtime_error(mocker):
        mocker.patch.object(
            stub_usb.core.Device,
            'is_kernel_driver_active',
            return_value=True
        )
        mocker.patch.object(
            stub_usb.core.Device,
            'detach_kernel_driver',
            side_effect=stub_usb.core.USBError('Mocked usb error')
        )

        with pytest.raises(RuntimeError):
            ct = Sm.SpaceMouseProWireless()

    @staticmethod
    def test_interrupt_msg_timeout_returns_one(mocker, mock_ct):
        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            side_effect=stub_usb.core.USBError('Timeout', errno=110)
        )
        ret = mock_ct.get_interrupt_msg()

        assert ret == 1

    @staticmethod
    def test_usb_read_fails_raises_usb_error(mocker, mock_ct):
        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            side_effect=stub_usb.core.USBError('Undefined USB Error')
        )

        with pytest.raises(stub_usb.core.USBError):
            mock_ct.get_interrupt_msg()


class TestButtonsAndJoystick:
    # ===================== Tests ==========================================
    @staticmethod
    def test_joystick_not_touched_sets_joystick_param_values_to_none(mocker, mock_ct):
        # First index shows type of msg, 1 == joystick
        msg = array.array('i', [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        for key in mock_ct.paramKeyList[:6]:
            assert mock_ct.paramDict[key] is None

    @staticmethod
    def test_buttons_not_pressed_sets_button_param_values_to_false(mocker, mock_ct):
        # First index shows type of msg, 3 == buttons
        msg = array.array('i', [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        for key in mock_ct.paramKeyList[6:]:
            assert mock_ct.paramDict[key] is False

    @staticmethod
    def test_press_button_does_not_reset_joystick(mocker, mock_ct):
        # First index shows type of msg, 1 == joystick. Non-zero position.
        msg = array.array('i', [1, 0, 0, 250, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # First index shows type of msg, 3 == button. "Shift" button pressed.
        msg = array.array('i', [3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # Button "Right"
        assert mock_ct.paramDict['shift'] is True

        # Joystick
        for key in mock_ct.paramKeyList[:6]:
            assert mock_ct.paramDict[key] is not None

    @staticmethod
    def test_release_all_button_does_not_reset_joystick(mocker, mock_ct):
        # First index shows type of msg, 1 == joystick. Non-zero position.
        msg = array.array('i', [1, 0, 0, 250, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # First index shows type of msg, 3 == button. All buttons released.
        msg = array.array('i', [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # All buttons released
        for key in mock_ct.paramKeyList[6:]:
            assert mock_ct.paramDict[key] is False

        # Joystick should be moved and therefore show values, not None.
        for key in mock_ct.paramKeyList[:6]:
            assert mock_ct.paramDict[key] is not None

    @staticmethod
    def test_release_one_button_while_other_pressed_does_not_reset_joystick(mocker, mock_ct):
        # First index shows type of msg, 1 == joystick. Non-zero position.
        msg = array.array('i', [1, 0, 0, 250, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # First index shows type of msg, 3 == button. "Front, Right" buttons pressed.
        msg = array.array('i', [0x3, 0b00110000, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # First index shows type of msg, 3 == button. Right released, front pressed.
        msg = array.array('i', [0x3, 0b00100000, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # Front pressed, right released
        assert mock_ct.paramDict['front'] is True
        assert mock_ct.paramDict['right'] is False

        # Joystick should be moved and therefore show values, not None.
        for key in mock_ct.paramKeyList[:6]:
            assert mock_ct.paramDict[key] is not None

    @staticmethod
    def test_release_joystick_does_not_reset_buttons(mocker, mock_ct):
        # First index shows type of msg, 1 == joystick. Non-zero position.
        msg = array.array('i', [1, 0, 0, 250, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # First index shows type of msg, 3 == button. "Front, Right" buttons pressed.
        msg = array.array('i', [0x3, 0b00110000, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # First index shows type of msg, 1 == joystick. Joystick released.
        msg = array.array('i', [0x1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # Front pressed, right pressed
        assert mock_ct.paramDict['front'] is True
        assert mock_ct.paramDict['right'] is True

        # Joystick should be released
        for key in mock_ct.paramKeyList[:6]:
            assert mock_ct.paramDict[key] is None

    @staticmethod
    def test_move_joystick_from_neutral_does_not_reset_buttons(mocker, mock_ct):
        # First index shows type of msg, 3 == button. "Front, Right" buttons pressed.
        msg = array.array('i', [0x3, 0b00110000, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # First index shows type of msg, 1 == joystick. Non-zero position.
        msg = array.array('i', [1, 0, 0, 250, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # Front pressed, right released
        assert mock_ct.paramDict['front'] is True
        assert mock_ct.paramDict['right'] is True

        # Joystick should be moved and therefore show values, not None.
        for key in mock_ct.paramKeyList[:6]:
            assert mock_ct.paramDict[key] is not None

    @staticmethod
    def test_all_buttons_pressed_sets_all_buttons_to_true(mocker, mock_ct):
        # First index shows type of msg, 3 == button. "Front, Right" buttons pressed.
        msg = array.array('i', [0x3, 0xFF, 0xFF, 0xFF, 0xFF])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        for key in mock_ct.paramKeyList[6:]:
            assert mock_ct.paramDict[key] is True

    @staticmethod
    def test_joystick_goes_to_negative_values(mocker, mock_ct):
        # x-Axis inverted in device by manufacturer (all axes set to -90 deg by this message).
        msg = array.array('i', [1, 0xA6, 0xFF, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        for item in mock_ct.paramKeyList[:6]:
            assert mock_ct.paramDict[item] == -90

    @staticmethod
    def test_3_buttons_simultaneous_shows_only_correct_buttons_in_dict(mocker, mock_ct):
        # First index shows type of msg, 3 == button. "Front, Right, Top" buttons pressed.
        msg = array.array('i', [0x3, 0b00110100, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        pressedButtons = ['front', 'right', 'top']
        for key in mock_ct.paramKeyList[6:]:
            if key in pressedButtons:
                assert mock_ct.paramDict[key] is True
            else:
                assert mock_ct.paramDict[key] is False

    @staticmethod
    def test_5_buttons_simultaneous_shows_only_correct_buttons_in_dict(mocker, mock_ct):
        # First index shows type of msg, 3 == button. "Front, Right, Top" buttons pressed.
        msg = array.array('i', [0x3, 0b00110000, 0, 0, 0b111])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        pressedButtons = ['lockRotation', 'control', 'shift', 'front', 'right']
        for key in mock_ct.paramKeyList[6:]:
            if key in pressedButtons:
                assert mock_ct.paramDict[key] is True
            else:
                assert mock_ct.paramDict[key] is False


class TestUsbMessageHandling:
    @staticmethod
    def test_usb_msg_type_22_recognised(mocker, mock_ct):
        msg = array.array('i', [22, 0xA6, 0xFF, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00])

        previousDict = mock_ct.paramDict.copy()

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # no parameter has changed in the dictionary because message type 22 is dropped
        for key in mock_ct.paramKeyList:
            assert previousDict[key] == mock_ct.paramDict[key]

    @staticmethod
    def test_usb_msg_type_23_recognised(mocker, mock_ct):
        msg = array.array('i', [23, 0xA6, 0xFF, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00, 0x5A, 0x00])

        previousDict = mock_ct.paramDict.copy()

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        mock_ct.get_interrupt_msg()

        # no parameter has changed in the dictionary because message type 22 is dropped
        for key in mock_ct.paramKeyList:
            assert previousDict[key] == mock_ct.paramDict[key]

    @staticmethod
    def test_usb_msg_type_0_raises_value_error(mocker, mock_ct):
        msg = array.array('i', [0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        with pytest.raises(ValueError):
            mock_ct.get_interrupt_msg()

    @staticmethod
    def test_multiple_msgs_same_button_pressed_accepted(mocker, mock_ct):
        # "Front" button pressed.
        msg = array.array('i', [0x3, 0b00100000, 0, 0, 0])

        mocker.patch.object(
            stub_usb.core.Device,
            'read',
            return_value=msg
        )

        # Multiple messages for same button (continuous press)
        mock_ct.get_interrupt_msg()
        mock_ct.get_interrupt_msg()
        mock_ct.get_interrupt_msg()

        assert mock_ct.paramDict['front'] is True


if __name__ == '__main__':
    sys.exit(pytest.main())
