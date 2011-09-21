import logging
import ctypes

class Hotkey(object):

    def __init__(self, keyId, modifiers, virtualkeys, execute):

        self.keyId = keyId 
        self.modifiers = modifiers
        self.virtualkeys = virtualkeys
        self.execute = execute

    def register(self, window):
        """
        Registers the hotkeys into windows
        Returns true on success
        Returns false on error
        """

        if ctypes.windll.user32.RegisterHotKey(window.hWindow
                ,self.keyId
                ,self.modifiers
                ,self.virtualkeys):

            return True

        else:

            return False

    def unregister(self, window):
        """
        Unregisters the hotkeys that are created on initialization
        """

        ctypes.windll.user32.UnregisterHotKey (window.hWindow, self.keyId)
