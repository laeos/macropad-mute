import displayio
import terminalio
import usb_hid
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_macropad import MacroPad

import hid_callcontrol


class Key:
    __slots__ = ["label"]

    def __init__(self, label):
        self.label = label

    def pushed(self):
        pass

    def released(self):
        pass

    def poll(self, macropad, key):
        return


class Macro(Key):
    __slots__ = ["_codes"]

    def __init__(self, label, codes):
        super().__init__(label)
        self._codes = codes


class KC(Macro):
    def pressed(self, macropad):
        for key in self._codes:
            macropad.keyboard.press(key)
        macropad.keyboard.release_all()


class CC(Macro):
    def pressed(self, macropad):
        for key in self._codes:
            macropad.consumer_control.send(key)


class Mute(Key):
    def pressed(self, macropad):
        muter.toggle_mute()

    def poll(self, macropad, key):
        if muter.has_report:
            if muter.in_meeting:
                if muter.muted:
                    macropad.pixels[key] = (255, 0, 0)
                else:
                    macropad.pixels[key] = (0, 255, 0)
            else:
                macropad.pixels[key] = (0, 0, 0)
        else:
            macropad.pixels[key] = (0, 0, 255)


shortcut_keys = {
    "macros": [
        # 1st row ----------
        KC("Esc", [MacroPad.Keycode.ESCAPE]),
        KC("Tab", [MacroPad.Keycode.TAB]),
        CC("Vol+", [MacroPad.ConsumerControlCode.VOLUME_INCREMENT]),
        # 2nd row ----------
        CC("Play", [MacroPad.ConsumerControlCode.PLAY_PAUSE]),
        KC("Home", [MacroPad.Keycode.HOME]),
        CC("Vol-", [MacroPad.ConsumerControlCode.VOLUME_DECREMENT]),
        # 3rd row ----------
        KC("End", [MacroPad.Keycode.END]),
        KC("Copy", [MacroPad.Keycode.COMMAND, MacroPad.Keycode.C]),
        KC("Pg Up", [MacroPad.Keycode.PAGE_UP]),
        # 4th row ----------
        Mute("MUTE"),
        KC("Paste", [MacroPad.Keycode.COMMAND, MacroPad.Keycode.V]),
        KC("Pg Dn", [MacroPad.Keycode.PAGE_DOWN]),
    ]
}

macropad = MacroPad()
muter = hid_callcontrol.CallControl(usb_hid.devices, verbose=True)

# Setup title and grid
main_group = displayio.Group()
macropad.display.show(main_group)
title = label.Label(
    y=4,
    font=terminalio.FONT,
    color=0x0,
    text="      SHORTCUTS       ",
    background_color=0xFFFFFF,
)
layout = GridLayout(x=0, y=10, width=128, height=44, grid_size=(3, 4), cell_padding=5)

# Extract data from shortcuts
label_names = [obj.label for obj in shortcut_keys["macros"]]
macros = shortcut_keys["macros"]

# Generate the labels based on the label names and add them to the appropriate grid cell
labels = []
for index in range(12):
    x = index % 3
    y = index // 3
    labels.append(label.Label(terminalio.FONT, text=label_names[index]))
    layout.add_content(labels[index], grid_position=(x, y), cell_size=(1, 1))

# Display the text
main_group.append(title)
main_group.append(layout)

macropad.pixels.fill(0)
macropad.stop_tone()

while True:
    key_event = macropad.keys.events.get()  # Begin checking for key events.
    if key_event:  # If there is a key event, e.g. a key has been pressed...
        if key_event.pressed:  # And a key is currently being pressed...
            macro = macros[key_event.key_number]
            if macro:
                macro.pressed(macropad)

    for key, macro in enumerate(macros):
        macro.poll(macropad, key)
