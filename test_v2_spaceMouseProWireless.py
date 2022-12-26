"""
V2: Try to write tests only on public functions, targeting functionality.
-> Otherwise refactoring becomes impossible because every function is fixed.
"""

import pytest
import sys

import usb.core
from stub_usb.stub_usb import Device as Stub_Device

import spaceMouseProWireless as Sm


class TestUsbConnectionEstablishment:

    # ===================== Fixtures =======================================
    @staticmethod
    @pytest.fixture(scope='class')
    def mock_usb_core_find(class_mocker):
        class_mocker.patch(
            'usb.core.find',
            return_value=Stub_Device()
        )

    @staticmethod
    @pytest.fixture(autouse=True, scope='function')
    def mock_usb_dispose(mocker):
        mocker.patch(
            'usb.util.dispose_resources',
            return_value=None
        )

    @staticmethod
    @pytest.fixture(scope='function')
    def mock_ct(mock_usb_core_find):
        ct = Sm.SpaceMouseProWireless()

        return ct

    @staticmethod
    @pytest.fixture(scope='class')
    def mock_usb(class_mocker):
        class_mocker.patch.object() # USB-package mocked as a whole

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
        assert mock_ct._dev.msg == Stub_Device().msg

    @staticmethod
    def test_usb_is_kernel_driver_active_is_verified(mocker, mock_usb_core_find):
        mocker.patch.object(Stub_Device, 'is_kernel_driver_active')

        ct = Sm.SpaceMouseProWireless()
        ct._dev.is_kernel_driver_active.assert_called_once()

    @staticmethod
    def test_usb_detach_kernel_driver_fails_raises_runtime_error(mocker, mock_usb_core_find):
        mocker.patch.object(Stub_Device, 'is_kernel_driver_active', return_value=True)
        mocker.patch.object(Stub_Device, 'detach_kernel_driver', side_effect=usb.core.USBError('Mocked usb error'))

        with pytest.raises(RuntimeError):
            ct = Sm.SpaceMouseProWireless()



if __name__ == '__main__':
    sys.exit(pytest.main())
