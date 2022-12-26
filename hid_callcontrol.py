#
# Call control!
#

import binascii
import struct

import adafruit_hid
import usb_hid

_USAGE = 0x5  # Telephony
_USAGE_PAGE = 0xB  # Handset
_REPORT_ID = 0xA

# fmt: off
# Generated with Waratah and its telephonyHeadset example.
_REPORT_DESCRIPTOR = bytes((
    0x05, 0x0B,  # UsagePage(Telephony Device[11])  # noqa
    0x09, 0x05,  # UsageId(Headset[5])  # noqa
    0xA1, 0x01,  # Collection(Application)  # noqa
    0x85, _REPORT_ID,  #     ReportId(1)  # noqa
    0x09, 0x2F,  #     UsageId(Phone Mute[47])  # noqa
    0x15, 0x00,  #     LogicalMinimum(0)  # noqa
    0x25, 0x01,  #     LogicalMaximum(1)  # noqa
    0x95, 0x01,  #     ReportCount(1)  # noqa
    0x75, 0x01,  #     ReportSize(1)  # noqa
    0x81, 0x02,  #     Input(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, BitField)  # noqa
    0x09, 0x20,  #     UsageId(Hook Switch[32])  # noqa
    0x81, 0x02,  #     Input(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, BitField)  # noqa
    0x75, 0x06,  #     ReportSize(6)  # noqa
    0x81, 0x03,  #     Input(Constant, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, BitField)  # noqa
    0x05, 0x08,  #     UsagePage(LED[8])  # noqa
    0x09, 0x17,  #     UsageId(Off-Hook[23])  # noqa
    0x75, 0x01,  #     ReportSize(1)  # noqa
    0x91, 0x02,  #     Output(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, NonVolatile, BitField)  # noqa
    0x09, 0x09,  #     UsageId(Mute[9])  # noqa
    0x91, 0x02,  #     Output(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, NonVolatile, BitField)  # noqa
    0x09, 0x21,  #     UsageId(Microphone[33])  # noqa
    0x91, 0x02,  #     Output(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, NonVolatile, BitField)  # noqa
    0x09, 0x18,  #     UsageId(Ring[24])  # noqa
    0x91, 0x02,  #     Output(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, NonVolatile, BitField)  # noqa
    0x75, 0x04,  #     ReportSize(4)  # noqa
    0x91, 0x03,  #     Output(Constant, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, NonVolatile, BitField)  # noqa
    0xC0,        # EndCollection()  # noqa
))
# fmt: on


class CallControl:
    __slots__ = [
        "_device",
        "_report",
        "_last_report",
        "_muted",
        "_hangup",
        "_in_meeting",
        "_reported",
        "_verbose",
    ]

    def __init__(self, devices, verbose=False):
        # NOTE: send_report prepends a report ID IFF it is present in the descriptor
        # so this should be the DATA only!
        report_length = 1

        self._device = adafruit_hid.find_device(
            devices, usage_page=_USAGE_PAGE, usage=_USAGE
        )
        self._report = bytearray(report_length)
        self._last_report = bytearray(report_length)
        self._muted = False
        self._hangup = False
        self._in_meeting = False
        self._reported = False
        self._verbose = False

    def toggle_mute(self):
        self._muted = not self._muted
        self._send()

    def set_mute(self, state):
        self._muted = state
        self._send()

    def set_hookswitch(self, state):
        self._hangup = state
        self._send()

    def _send(self):
        report = 0
        if self._hangup:
            report += 0x2
        if self._muted:
            report += 0x1

        struct.pack_into("<B", self._report, 0, report)

        if True or self._last_report != self._report:
            if self._verbose:
                print("REPORT " + str(binascii.hexlify(self._report)))
            self._device.send_report(self._report)
            self._last_report[:] = self._report

    def _poll(self):
        data = self._device.get_last_received_report()
        if data:
            self._reported = True
            if self._verbose:
                print("RX REPORT: " + str(binascii.hexlify(data)))
            if data[0] & 0x1:
                self._in_meeting = True
            else:
                self._in_meeting = False

            if data[0] & 0x2:
                self._muted = True
            else:
                self._muted = False

    @property
    def has_report(self):
        self._poll()
        return self._reported

    @property
    def in_meeting(self):
        self._poll()
        return self._in_meeting

    @property
    def muted(self):
        self._poll()
        return self._muted

    @staticmethod
    def hid_device():
        return usb_hid.Device(
            report_descriptor=_REPORT_DESCRIPTOR,
            usage_page=_USAGE_PAGE,
            usage=_USAGE,
            report_ids=(_REPORT_ID,),  # Single report
            in_report_lengths=(1,),  # One byte reports (should not include report ID)
            out_report_lengths=(1,),  # One byte OUT report
        )
