import ctypes

from win32con import WM_HOTKEY
from win32con import PM_REMOVE

class HotkeyController(object):

    def __init__(self, hotkeys, hotkeyhandlers, window):

        self.hotkeys = hotkeys
        self.hotkeyhandlers = hotkeyhandlers
        self.window = window

    def register_hotkeys(self):
        "Registers the hotkeys that are created on initialization"

        for i, (modifiers, vk) in self.hotkeys.items():

            if not ctypes.windll.user32.RegisterHotKey(self.window, i, modifiers, vk):

                print ("Unable to register id ", i)

            else:

                print ("Finished registering id: ", i)

    def unregister_hotkeys(self):
        "Unregisters the hotkeys that are created on initialization"

        for i, (modifiers, vk) in self.hotkeys.items():

            print ("Unregistering key: ", modifiers, vk)
            ctypes.windll.user32.UnregisterHotKey (self.window, i)
