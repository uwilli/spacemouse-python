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


class TestUsbMessageHandling:
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


if __name__ == '__main__':
    sys.exit(pytest.main())
