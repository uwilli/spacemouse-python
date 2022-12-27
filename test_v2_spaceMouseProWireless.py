"""
V2: Try to write tests only on public functions, targeting functionality.
-> Otherwise refactoring becomes impossible because every function is fixed.
"""

import pytest
import sys

import spaceMouseProWireless as Sm
import stub_usb.core


class TestUsbConnectionEstablishment:

    # ===================== Fixtures =======================================
    @staticmethod
    @pytest.fixture(scope='function')
    def mock_ct():
        ct = Sm.SpaceMouseProWireless()

        return ct

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
        mocker.patch.object(stub_usb.core.Device, 'is_kernel_driver_active')

        ct = Sm.SpaceMouseProWireless()
        ct._dev.is_kernel_driver_active.assert_called_once()

    @staticmethod
    def test_usb_detach_kernel_driver_fails_raises_runtime_error(mocker):
        mocker.patch.object(stub_usb.core.Device, 'is_kernel_driver_active', return_value=True)
        mocker.patch.object(stub_usb.core.Device, 'detach_kernel_driver', side_effect=stub_usb.core.USBError('Mocked usb error'))

        with pytest.raises(RuntimeError):
            ct = Sm.SpaceMouseProWireless()



if __name__ == '__main__':
    sys.exit(pytest.main())
