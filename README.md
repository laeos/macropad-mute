Mostly just a hardware mute button for google meet using USB HID Call Control
interface (this means it actually syncs with meet!).

To use: 
- install the code
- reset/unplug and plugin the device (to make sure boot.py re-executes and the HID device is setup)
- in chrome, in google meet, in settings under the audio tab, pair the call control device
    - mine shows up as `Macropad RP2040`

## NOTES

usb\_hid send\_report prepends report ID (maybe unless you 
explicitly pass it zero?) so don't include that byte in any
of the sizes or in the report data.

* [adafruit\_hid](https://github.com/adafruit/Adafruit_CircuitPython_HID/tree/main/adafruit_hid)
* [usb descriptor decoder](https://eleccelerator.com/usbdescreqparser/)
* [usb hid tables](https://www.usb.org/hid)
* [Waratah - hid compiler](https://github.com/microsoft/hidtools)
* [custom HID in circuitpython](https://learn.adafruit.com/custom-hid-devices-in-circuitpython?view=all)
* [call state management HID](https://www.usb.org/sites/default/files/hutrr106-callstatemanagementcontrol_0.pdf)
* [system mic mute](https://www.usb.org/sites/default/files/hutrr110-systemmicrophonemute.pdf)

