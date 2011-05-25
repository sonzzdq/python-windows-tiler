import ctypes
from ctypes import wintypes

from win32con import WM_HOTKEY

byref = ctypes.byref
user32 = ctypes.windll.user32

class HotkeyListener:

    def __init__(self, hotkeys, hotkeyhandlers):

        self.hotkeys = hotkeys;
        self.hotkeyhandlers = hotkeyhandlers

    def register_hotkeys(self):
        "Registers the hotkeys that are created on initialization"

        for i, (modifiers, vk) in self.hotkeys.items():

            print ("Registering key: ", modifiers, vk)

            if not user32.RegisterHotKey (None, i, modifiers, vk):

                print ("Unable to register id ", i)
                pass

            else:

                print ("Finished registering id: ", i)
                pass

    def unregister_hotkeys(self):
        "Unregisters the hotkeys that are created on initialization"

        for i, (modifiers, vk) in self.hotkeys.items():

            print ("Unregistering key: ", modifiers, vk)
            user32.UnregisterHotKey (None, i)

    def listen_to_hotkeys(self):
        "Listens to the hotkeys that are created on initialization"

        #register the hotkeys
        self.register_hotkeys()

        try:

            #define msg
            msg = wintypes.MSG()

            #wait for a message
            while user32.GetMessageA(byref(msg), None, 0, 0) != 0:

                #check if message is a hotkey and if we have it registered
                if msg.message == WM_HOTKEY and msg.wParam in self.hotkeyhandlers.keys():

                    #execute the hotkey handler in a different thread (smooth actions when hotkey is rapidly pressed)
                    self.hotkeyhandlers.get(msg.wParam)()

                #user32.TranslateMessage(byref(msg))
                #user32.DispatchMessageA(byref(msg))
        finally:

            #unregister the hotkeys
            self.unregister_hotkeys()

