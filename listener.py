from hotkeylistener import HotkeyListener
from windowlistener import WindowListener

import time

class Listener():

    def __init__(self, hotkeys, hotkeyhandlers, floats, windowhandler):
        "create the hotkey and window listeners on initialization"

        self.stop = False
        self.hotkeylistener = HotkeyListener(hotkeys, hotkeyhandlers)
        self.windowlistener = WindowListener(floats)
        self.windowhandler = windowhandler

    def start(self):
        "start the listeners with a safety try/finally to unregister keys"

        print("start")
        self.hotkeylistener.register_hotkeys()

        try:

            while not self.stop:

                "Sleep for 0.05 to save resources"
                time.sleep(0.05)

                "Use the listeners"
                self.hotkeylistener.handle_keypress()
                self.windowlistener.handle_window_event(self.windowhandler)

        finally:

            print("stop")

            self.hotkeylistener.unregister_hotkeys()
