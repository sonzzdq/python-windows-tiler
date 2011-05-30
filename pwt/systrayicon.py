#!/usr/bin/env python
# Module     : SysTrayIcon.py
# Synopsis   : Windows System tray icon.
# Programmer : Simon Brunning - simon@brunningonline.net
# Date       : 11 April 2005
# Notes      : Based on (i.e. ripped off from) Mark Hammond's
#              win32gui_taskbar.py and win32gui_menu.py demos from PyWin32
# Modified   : Bob Reynders - tzbob@hotmail.com
#              Stripped it down to suit my own needs, formatted code and made it Python3 friendly 

         
import os
import win32api
import win32con
try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

class SysTrayIcon(object):
    "Object representing a systemtrayicon on windows"
    
    def __init__(self, icon, hover_text, window_class_name):
        
        self.icon = icon
        self.hover_text = hover_text
        self.window_class_name = window_class_name
        
        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        classAtom = win32gui.RegisterClass(window_class)

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom,
                                          self.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)

        win32gui.UpdateWindow(self.hwnd)

        self.notify_id = None
        self.refresh_icon()
       
    def refresh_icon(self, icon=None):

        if icon:
            
            self.icon = icon

        # Try and find a custom icon
        hinst = win32gui.GetModuleHandle(None)

        if os.path.isfile(self.icon):

            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)

        else:

            print("Can't find icon file - using default.")
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id: 

            message = win32gui.NIM_MODIFY

        else: 
            
            message = win32gui.NIM_ADD

        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER+20,
                          hicon,
                          self.hover_text)

        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def destroy(self):

        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
