#Cx_Frozen .exe's throw errors without re?
import re
import time
import os
import threading

import windowutilities

from listener import Listener
from tiler import Tiler

from win32con import MOD_ALT
from win32con import MOD_SHIFT
from win32con import VK_RETURN

stop = False

def handler_alt_shift_C():
    "Handles alt+shift+C, closes the current window"

    window = windowutilities.get_focused_window()

    #only remove the window from the tiler if it is in the tiler
    if window in tiler.windows:

        tiler.windows.remove(window)
        windowpoll.oldAmount -= 1

    #close and retile
    windowutilities.close(window)
    tiler.tile_windows()

def handler_alt_shift_V():
    "Handles alt+shift+V, minimizes the current window"

    window = windowutilities.get_focused_window()

    #only remove the window from the tiler if it is in the tiler
    if window in tiler.windows:

        tiler.windows.remove(window)
        windowpoll.oldAmount -= 1

    #minimize and retile
    windowutilities.minimize(window)
    tiler.tile_windows()

def handler_alt_shift_Q():
    "Handles alt+shift+Q, quits the application"

    #stop the polls
    listener.stop = True

if __name__ == "__main__":

    #initialization

    tiler = Tiler()

    #create <<classname>> based ignorelist
    floats = (#This list may hurt performance if it's huge
            #"progman"			#example
            #, "progman"		#example
            )

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
    hotkeyhandlers = {1: tiler.decrease_masterarea_width
            , 2:  tiler.increase_masterarea_width
            , 3:  tiler.set_focus_down
            , 4:  tiler.set_focus_up
            , 5:  tiler.move_focusedwindow_down
            , 6:  tiler.move_focusedwindow_up
            , 7:  tiler.move_focusedwindow_to_masterarea
            , 8:  tiler.decrease_masterarea_size
            , 9:  tiler.increase_masterarea_size
            , 10:  handler_alt_shift_C
            , 11:  handler_alt_shift_V
            , 12:  handler_alt_shift_Q
            }

    listener = Listener(hotkeys, hotkeyhandlers, floats, tiler.tile_windows)

    listener.start()

