import ctypes
from ctypes import wintypes

import time

from win32con import WM_HOTKEY
from win32con import PM_REMOVE

byref = ctypes.byref
user32 = ctypes.windll.user32

class HotkeyListener:

    def __init__(self, hotkeys, hotkeyhandlers):

        self.hotkeys = hotkeys
        self.hotkeyhandlers = hotkeyhandlers
        self.stop = False 
        self.msg = wintypes.MSG()

    def register_hotkeys(self):
        "Registers the hotkeys that are created on initialization"

        for i, (modifiers, vk) in self.hotkeys.items():

            print ("Registering key: ", modifiers, vk)

            if not user32.RegisterHotKey (None, i, modifiers, vk):

                print ("Unable to register id ", i)

            else:

                print ("Finished registering id: ", i)

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
            while not self.stop:

                time.sleep(0.1)

                if user32.PeekMessageA(byref(msg), None, WM_HOTKEY, WM_HOTKEY, PM_REMOVE):

                    #check if message is a hotkey and if we have it registered
                    if msg.wParam in self.hotkeyhandlers.keys():

                        #execute the hotkey handler
                        self.hotkeyhandlers.get(msg.wParam)()

                    user32.TranslateMessage(byref(msg))
                    user32.DispatchMessageA(byref(msg))

        finally:

            #unregister the hotkeys
            self.unregister_hotkeys()

    def handle_keypress(self):
        "Listens to the hotkeys that are created on initialization"

        #define msg

        if user32.PeekMessageA(byref(self.msg), None, WM_HOTKEY, WM_HOTKEY, PM_REMOVE):

            #check if message is a hotkey and if we have it registered
            if self.msg.wParam in self.hotkeyhandlers.keys():

                #execute the hotkey handler
                self.hotkeyhandlers.get(self.msg.wParam)()

            user32.TranslateMessage(byref(self.msg))
            user32.DispatchMessageA(byref(self.msg))


