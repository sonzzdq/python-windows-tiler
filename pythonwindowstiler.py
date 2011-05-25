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

def handler_alt_H():
    "Handles alt+H, decreases the masterwidth"

    #decrease master areaWidth 
    tilehandler.masterareaWidth -= 100
    print("master area -= 100")

    tilehandler.tile_windows()

def handler_alt_L():
    "Handles alt+L, increases the masterwidth"

    #increase master areaWidth 
    tilehandler.masterareaWidth += 100
    print("master area += 100")

    tilehandler.tile_windows()

def handler_alt_J():
    "Handles alt+J, sets focus on the next window"

    #get focused window
    foregroundWindow = windowutilities.get_focused_window()

    #only grab and move the focus if it is in the tilehandler
    if foregroundWindow in tilehandler.windows:

        i = tilehandler.windows.index(foregroundWindow) + 1

        #if the index after the foreground's is out of range, assign 0
        if i >= len(tilehandler.windows):

            i = 0

        #focus window and cursor
        windowutilities.focus(tilehandler.windows[i])
        windowutilities.set_cursor_window(tilehandler.windows[i])

        print ("change focus down")

def handler_alt_K():
    "Handles alt+K, sets focus on the previous window"

    #get focused window
    foregroundWindow = windowutilities.get_focused_window()

    #only grab and move the focus if it is in the tilehandler
    if foregroundWindow in tilehandler.windows:

        i = tilehandler.windows.index(foregroundWindow) - 1

        #if the index before the foreground's is out of range, assign last index
        if i < 0:

            i = len(tilehandler.windows) - 1

        #focus window and cursor
        windowutilities.focus(tilehandler.windows[i])
        windowutilities.set_cursor_window(tilehandler.windows[i])

        print ("change focus up")

def handler_alt_shift_J():
    "Handles alt+shift+J, switches the window to the next position"

    #get focused window
    foregroundWindow = windowutilities.get_focused_window()

    #only grab and move the window if it is in the tilehandler
    if foregroundWindow in tilehandler.windows:

        i = tilehandler.windows.index(windowutilities.get_focused_window())

        #if the foreground window is the last window, shift everything and place it first
        if i == len(tilehandler.windows) - 1:

            tilehandler.windows[0], tilehandler.windows[1:] = tilehandler.windows[i], tilehandler.windows[:i]

        #else shift it with the following window
        else:

            tilehandler.windows[i], tilehandler.windows[i + 1] = tilehandler.windows[i + 1], tilehandler.windows[i]

        print ("change order down")
        tilehandler.tile_windows()

def handler_alt_shift_K():
    "Handles alt+shift+K, switches the window to the previous position"

    foregroundWindow = windowutilities.get_focused_window()

    #only grab and move the window if it is in the tilehandler
    if foregroundWindow in tilehandler.windows:

        i = tilehandler.windows.index(windowutilities.get_focused_window())

        #if the foreground window is first, shift everything and place it last
        if i == 0:

            j = len(tilehandler.windows) - 1
            tilehandler.windows[j], tilehandler.windows[:j] = tilehandler.windows[0], tilehandler.windows[1:]

        #else shift it with the trailing window
        else:

            j = i - 1
            tilehandler.windows[i], tilehandler.windows[j] = tilehandler.windows[j], tilehandler.windows[i]

        print ("change order up")
        tilehandler.tile_windows()

def handler_alt_shift_L():
    "Handles alt+shift+L, decreases the masterarea size"

    #decrease the masterarea size if it's possible
    if tilehandler.masterareaSize > 1:

        tilehandler.masterareaSize -= 1

        print ("masterarea size -= 1")
        tilehandler.tile_windows()

def handler_alt_shift_H():
    "Handles alt+shift+H, increases the masterarea size"

    #increase the masterarea size if it's possible
    if tilehandler.masterareaSize < len(tilehandler.windows):

        tilehandler.masterareaSize += 1

        print ("masterarea size += 1")
        tilehandler.tile_windows()

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

    #unregister hotkeys and exit app
    hotkeypoll.unregister_hotkeys()

    os._exit(0)

if __name__ == "__main__":

    #create <<classname>> based ignorelist
    ignoreList = (#This list may hurt performance if it's huge
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
            , 7: (MOD_ALT + MOD_SHIFT, ord("L"))
            , 8: (MOD_ALT + MOD_SHIFT, ord("H"))
            , 9: (MOD_ALT + MOD_SHIFT, ord("C"))
            , 10: (MOD_ALT + MOD_SHIFT, ord("V"))
            , 11: (MOD_ALT + MOD_SHIFT, ord("Q"))
            }

    #list the corresponding handlers 
    hotkeyhandlers = {1: handler_alt_H
            , 2:  handler_alt_L
            , 3:  handler_alt_J
            , 4:  handler_alt_K           
            , 5:  handler_alt_shift_J
            , 6:  handler_alt_shift_K
            , 7:  handler_alt_shift_L
            , 8:  handler_alt_shift_H
            , 9:  handler_alt_shift_C
            , 10:  handler_alt_shift_V
            , 11:  handler_alt_shift_Q
            }

    #initialization
    hotkeypoll = hotkeylistener.HotkeyListener(hotkeys, hotkeyhandlers)
    windowpoll = windowlistener.WindowListener(ignoreList)
    tilehandler = tiler.Tiler()

    #start a thread to listen to windows passing the tile_windows command 
    #tile_windows() will be launched when a new window is caught
    w = threading.Thread(name="Windowlistener", target=windowpoll.listen_to_windows, args=(tilehandler.tile_windows,))
    h = threading.Thread(name="Hotkeylistener", target=hotkeypoll.listen_to_hotkeys)

    #start the threads
    w.start()
    h.start()

    #wait for the threads 
    w.join()
    h.join()
