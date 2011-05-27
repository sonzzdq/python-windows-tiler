#Cx_Frozen .exe's throw errors without re?
import re

import os
import threading

import hotkeylistener
import windowlistener
import windowutilities
import tiler

from win32con import MOD_ALT
from win32con import MOD_SHIFT
from win32con import VK_RETURN

def handler_alt_shift_C():
    "Handles alt+shift+C, closes the current window"

    window = windowutilities.get_focused_window()

    #only remove the window from the tilehandler if it is in the tilehandler
    if window in tilehandler.windows:

        tilehandler.windows.remove(window)
        windowpoll.oldAmount -= 1

    #close and retile
    windowutilities.close(window)
    tilehandler.tile_windows()

def handler_alt_shift_V():
    "Handles alt+shift+V, minimizes the current window"

    window = windowutilities.get_focused_window()

    #only remove the window from the tiler if it is in the tiler
    if window in tilehandler.windows:

        tilehandler.windows.remove(window)
        windowpoll.oldAmount -= 1

    #minimize and retile
    windowutilities.minimize(window)
    tilehandler.tile_windows()

def handler_alt_shift_Q():
    "Handles alt+shift+Q, quits the application"

    #stop the polls
    hotkeypoll.stop = True
    windowpoll.stop = True

if __name__ == "__main__":

    #initialization

    tilehandler = tiler.Tiler()

    #create <<classname>> based ignorelist
    floatList = (#This list may hurt performance if it's huge
            #"progman"			#example
            #, "progman"		#example
            )

    windowpoll = windowlistener.WindowListener(floatList)

    #list the hotkeys that should be listened to
    hotkeys = {1: (MOD_ALT, ord("H"))
            , 2: (MOD_ALT, ord("L"))
            , 3: (MOD_ALT, ord("J"))
            , 4: (MOD_ALT, ord("K"))
            , 5: (MOD_ALT + MOD_SHIFT, ord("J"))
            , 6: (MOD_ALT + MOD_SHIFT, ord("K"))
            , 7: (MOD_ALT + MOD_SHIFT, VK_RETURN)
            , 8: (MOD_ALT + MOD_SHIFT, ord("L"))
            , 9: (MOD_ALT + MOD_SHIFT, ord("H"))
            , 10: (MOD_ALT + MOD_SHIFT, ord("C"))
            , 11: (MOD_ALT + MOD_SHIFT, ord("V"))
            , 12: (MOD_ALT + MOD_SHIFT, ord("Q"))
            }

    #list the corresponding handlers 
    hotkeyhandlers = {1: tilehandler.decrease_masterarea_width
            , 2:  tilehandler.increase_masterarea_width
            , 3:  tilehandler.set_focus_down
            , 4:  tilehandler.set_focus_up
            , 5:  tilehandler.move_focusedwindow_down
            , 6:  tilehandler.move_focusedwindow_up
            , 7:  tilehandler.move_focusedwindow_to_masterarea
            , 8:  tilehandler.increase_masterarea_size
            , 9:  tilehandler.decrease_masterarea_size
            , 10:  handler_alt_shift_C
            , 11:  handler_alt_shift_V
            , 12:  handler_alt_shift_Q
            }

    hotkeypoll = hotkeylistener.HotkeyListener(hotkeys, hotkeyhandlers)

    #start a thread to listen to windows passing the tile_windows command 
    #tile_windows() will be launched when a new window is caught
    w = threading.Thread(name="Windowlistener", target=windowpoll.listen_to_windows, args=(tilehandler.tile_windows,))
    h = threading.Thread(name="Hotkeylistener", target=hotkeypoll.listen_to_hotkeys)

    #start the threads
    w.start()
    h.start()
