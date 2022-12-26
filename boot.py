import usb_cdc
import usb_hid

import hid_callcontrol

# enable two serial ports: one for data, one for console
usb_cdc.enable(console=True, data=True)

usb_hid.enable(
    (
        hid_callcontrol.CallControl.hid_device(),
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.MOUSE,
        usb_hid.Device.CONSUMER_CONTROL,
    )
)
