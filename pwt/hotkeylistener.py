import ctypes
from ctypes import wintypes

from win32con import WM_HOTKEY
from win32con import PM_REMOVE

byref = ctypes.byref
user32 = ctypes.windll.user32

class HotkeyListener(object):

    def __init__(self, hotkeys, hotkeyhandlers):

        self.hotkeys = hotkeys
        self.hotkeyhandlers = hotkeyhandlers
        self.stop = False 
        self.msg = wintypes.MSG()

    def register_hotkeys(self):
        "Registers the hotkeys that are created on initialization"

        for i, (modifiers, vk) in self.hotkeys.items():

            if not user32.RegisterHotKey (None, i, modifiers, vk):

                print ("Unable to register id ", i)

            else:

                print ("Finished registering id: ", i)

    def unregister_hotkeys(self):
        "Unregisters the hotkeys that are created on initialization"

        for i, (modifiers, vk) in self.hotkeys.items():

            print ("Unregistering key: ", modifiers, vk)
            user32.UnregisterHotKey (None, i)

    def listen_to_keys(self):
        "Listens to the hotkeys that are created on initialization"

        #define msg

        if user32.PeekMessageA(byref(self.msg), None, WM_HOTKEY, WM_HOTKEY, PM_REMOVE):

            #check if message is a hotkey and if we have it registered
            if self.msg.wParam in self.hotkeyhandlers.keys():

                #execute the hotkey handler
                #self.hotkeyhandlers.get(self.msg.wParam)()
                self.hotkeyhandlers[self.msg.wParam]()

            user32.TranslateMessage(byref(self.msg))
            user32.DispatchMessageA(byref(self.msg))


