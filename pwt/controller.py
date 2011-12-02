from pwt.notifyicon     import NotifyIcon
from pwt.hotkey         import Hotkey
from pwt.monitor        import Monitor
from pwt.window         import Window
from pwt.taskbar        import Taskbar
from pwt.utility        import Utility

##KEYS
from win32con import MOD_ALT
from win32con import MOD_SHIFT
from win32con import VK_RETURN
from win32con import VK_DELETE
from win32con import VK_SPACE

##HOTKEY EVENTS
from win32con import WM_HOTKEY

##TILE EVENTS
from win32con import HSHELL_WINDOWCREATED
from win32con import HSHELL_WINDOWDESTROYED

class Controller(object):

    def __init__(self, name):
        """
        Set up the notifyicon and the monitors
        """

        self.group = 0

        self.ICONFOLDER = "icons/"

        #the events that trigger the removal of a window
        self.REMOVE_EVENTS = (HSHELL_WINDOWDESTROYED
                ,#placeholder
        )

        #the events that trigger an additional window
        self.ADD_EVENTS = (HSHELL_WINDOWCREATED
                ,#placeholder
        )

        #notifyicon
        self.notifyicon = NotifyIcon(name
                ,self.icon
        )

        self.add_hotkeys_to_notifyicon()
        self.notifyicon.register_hotkeys()

        self.notifyicon.register_shellhook() 

        self.taskbar = Taskbar()

        #monitors
        self.monitors = Monitor.display_monitors()

        if self.monitors is not None:

            self.stop = False

        else:

            self.stop = True

    @property
    def icon(self):
        "Return the appropriate icon"

        return self.ICONFOLDER + str(self.group + 1) + ".ico"

    @property
    def current_tiler(self):
        "Returns the current tiler"
        
        return Monitor.current_monitor_from_list(self.monitors).tilers[self.group]

    @property
    def groupwindows(self):
        "returns all the windows of the current group"

        windows = []

        for monitor in self.monitors:

            windows.extend(monitor.tilers[self.group].windows)

        return windows

    def start(self):
        "start the listeners with a safety try/finally to unregister keys and kill the icon"

        self.notifyicon.show_balloon("Go!", "PWT")

        #Do an initial lookup of all the windows and tile accordingly
        for monitor in self.monitors:

            monitor.tilers[self.group].windows = Window.valid_windows_from_monitor(monitor)
            monitor.tilers[self.group].tile_windows()

        try:

            #message priming read
            message = self.notifyicon.windowmessage

            while message:

                #if message is WM_HOTKEY
                if message[1][1] == WM_HOTKEY:

                    #execute the corresponding hotkeyhandler using the id
                    self.notifyicon.hotkeys[message[1][2] - 1].execute()

                #if lparam is an add event
                elif message[1][2] in self.ADD_EVENTS:

                    self.handle_add_event(Window(message[1][3]))
                    
                #if lparam is a remove event
                elif message[1][2] in self.REMOVE_EVENTS:

                    self.handle_remove_event(Window(message[1][3])
                            ,Monitor.monitor_from_point_in_list(self.monitors, message[1][5]))

                if self.stop:

                    self.notifyicon.show_balloon("Stop!", "PWT")
                    break

                #Grab the next message from the message queue
                message = self.notifyicon.windowmessage

        finally:

            #Unregister hotkeys and shellhook
            self.notifyicon.unregister_shellhook()
            self.notifyicon.unregister_hotkeys()

            #Decorate windows
            self.decorate_all_tiledwindows()

            #make sure the taskbar is shown on exit
            self.taskbar.show()

            #Remove icon
            self.notifyicon.destroy()

    def handle_add_event(self, window):
        "Triggered when a window has to be added"

        if window not in self.groupwindows and window.validate():

            tiler = self.current_tiler

            #undecorate and update the window
            window.undecorate()
            window.update()

            #append and tile retile the windows
            self.current_tiler.add_window(window)

    def handle_remove_event(self, window, monitor):
        "Triggered when a window needs to be removed"

        tiler = monitor.tilers[self.group]

        if window in tiler.windows:

            tiler.windows.remove(window)
            tiler.tile_windows()

    def decorate_all_tiledwindows(self):
        "Decorates all windows in the tiler's memory"

        for monitor in self.monitors:

            for tiler in monitor.tilers:

                for window in tiler.windows:

                    if not window.is_decorated():

                        window.decorate()

                    window.update()
                    window.show()

    def switch_group(self, i):
        "Switch the current group into group i"

        for monitor in self.monitors:

            for window in monitor.tilers[self.group].windows:

                window.hide()

            
            for window in monitor.tilers[i].windows:

                window.show()

            monitor.tilers[i].tile_windows()

        self.group = i
        self.notifyicon.draw_icon(self.icon)

        Window.window_under_cursor().focus()

    def send_window_to_tiler(self, window, i):
        "sends window to tiler i"

        currentMonitor = Monitor.monitor_from_window_in_list(self.monitors, window)
        currentTiler = currentMonitor.tilers[self.group] 
        targetTiler = currentMonitor.tilers[i] 

        #hide the window
        if window.validate():

            window.hide()

            #Remove window if it's in the tiler
            if window in currentTiler.windows:

                currentTiler.windows.remove(window)
                currentTiler.tile_windows()

            #Add window if it's not already in the target tiler
            if window not in targetTiler.windows:

                targetTiler.windows.append(window)

    ###
    #Hotkey handlers
    ###

    def handler_alt_H(self):
        "Handles alt+H, decreases the masterwidth"

        self.current_tiler.decrease_masterarea()

    def handler_alt_L(self):
        "Handles alt+L, increases the masterwidth"

        self.current_tiler.increase_masterarea()

    def handler_alt_J(self):
        "Handles alt+J, sets focus on the next window"

        self.current_tiler.focus_next()

    def handler_alt_K(self):
        "Handles alt+K, sets focus on the previous window"

        self.current_tiler.focus_previous()

    def handler_alt_return(self):
        "Handles alt+RETURN, sets focus on the masterarea"

        self.current_tiler.focus_primary()

    def handler_alt_shift_J(self):
        "Handles alt+shift+J, switches the window to the next position"

        self.current_tiler.move_focused_to_next()

    def handler_alt_shift_K(self):
        "Handles alt+shift+K, switches the window to the previous position"

        self.current_tiler.move_focused_to_previous()

    def handler_alt_shift_return(self):
        "Handles alt+shift+RETURN, switches the window to the masterarea"

        self.current_tiler.make_focused_primary()

    def handler_alt_shift_L(self):
        "Handles alt+shift+L, decreases the masterarea size"

        self.current_tiler.decrease_masterarea_size()

    def handler_alt_shift_H(self):
        "Handles alt+shift+H, increases the masterarea size"

        self.current_tiler.increase_masterarea_size()

    def handler_alt_shift_C(self):
        "Handles alt+shift+C, closes the current window"

        Window.focused_window().close()

    def handler_alt_one(self):
        "Handles alt+1, switches group"
        
        if self.group != 0:

            self.switch_group(0)

    def handler_alt_two(self):
        "Handles alt+2, switches group"
        
        if self.group != 1:

            self.switch_group(1)

    def handler_alt_three(self):
        "Handles alt+3, switches group"
        
        if self.group != 2:

            self.switch_group(2)

    def handler_alt_four(self):
        "Handles alt+4, switches group"
        
        if self.group != 3:

            self.switch_group(3)

    def handler_alt_five(self):
        "Handles alt+5, switches group"
        
        if self.group != 4:

            self.switch_group(4)

    def handler_alt_six(self):
        "Handles alt+6, switches group"
        
        if self.group != 5:

            self.switch_group(5)

    def handler_alt_seven(self):
        "Handles alt+7, switches group"
        
        if self.group != 6:

            self.switch_group(6)

    def handler_alt_eight(self):
        "Handles alt+8, switches group"
        
        if self.group != 7:

            self.switch_group(7)

    def handler_alt_nine(self):
        "Handles alt+9, switches group"
        
        if self.group != 8:

            self.switch_group(8)

    def handler_alt_shift_one(self):
        "Handles alt+shift+1, sends window to appropriate tiler"

        if self.group != 0:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 0)

    def handler_alt_shift_two(self):
        "Handles alt+shift+2, sends window to appropriate tiler"

        if self.group != 1:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 1)

    def handler_alt_shift_three(self):
        "Handles alt+shift+3, sends window to appropriate tiler"

        if self.group != 2:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 2)

    def handler_alt_shift_four(self):
        "Handles alt+shift+4, sends window to appropriate tiler"

        if self.group != 3:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 3)

    def handler_alt_shift_five(self):
        "Handles alt+shift+5, sends window to appropriate tiler"

        if self.group != 4:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 4)

    def handler_alt_shift_six(self):
        "Handles alt+shift+6, sends window to appropriate tiler"

        if self.group != 5:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 5)

    def handler_alt_shift_seven(self):
        "Handles alt+shift+7, sends window to appropriate tiler"

        if self.group != 6:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 6)

    def handler_alt_shift_eight(self):
        "Handles alt+shift+8, sends window to appropriate tiler"

        if self.group != 7:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 7)

    def handler_alt_shift_nine(self):
        "Handles alt+shift+9, sends window to appropriate tiler"

        if self.group != 8:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 8)

    def handler_alt_I(self):
        "Handles alt+I, changes focus to the next monitor"

        monitor = Monitor.current_monitor_from_list(self.monitors) 

        nextMonitor = Utility.next_item(self.monitors, monitor)

        if nextMonitor and nextMonitor.tilers[self.group].windows:

            window = nextMonitor.tilers[self.group].windows[0]

            if not window.focus():

                nextMonitor.tilers[self.group].remove_window(window)

    def handler_alt_U(self):
        "Handles alt+U, changes focus to the previous monitor"

        monitor = Monitor.current_monitor_from_list(self.monitors) 

        previousMonitor = Utility.previous_item(self.monitors, monitor)

        if previousMonitor and previousMonitor.tilers[self.group].windows:

            window = previousMonitor.tilers[self.group].windows[0]

            if not window.focus():

                previousMonitor.tilers[self.group].remove_window(window)

    def handler_alt_shift_I(self):
        "Handles alt+shift_I switches window to the next monitor"

        window = Window.focused_window()

        if window.validate():

            monitor = Monitor.monitor_from_window_in_list(self.monitors, window) 
            nextMonitor = Utility.next_item(self.monitors, monitor)

            if nextMonitor:
                
                tiler = monitor.tilers[self.group]
                nextTiler = nextMonitor.tilers[self.group]

                if window in tiler.windows:

                    tiler.remove_window(window)

                if window not in nextTiler.windows:

                    nextTiler.add_window(window)

                window.focus()

    def handler_alt_shift_U(self):
        "Handles alt+shift_U switches window to the previous monitor"

        window = Window.focused_window()

        if window.validate():

            monitor = Monitor.monitor_from_window_in_list(self.monitors, window) 
            previousMonitor = Utility.previous_item(self.monitors, monitor)

            if previousMonitor:
                
                tiler = monitor.tilers[self.group]
                previousTiler = previousMonitor.tilers[self.group]

                if window in tiler.windows:

                    tiler.remove_window(window)

                if window not in previousTiler.windows:

                    previousTiler.add_window(window)

                window.focus()

    def handler_alt_space(self):
        "Handles alt+space, grabs the next tile layout"

        self.current_tiler.next_layout()
        self.notifyicon.show_balloon(self.current_tiler.currentLayout.name
                ,"LAYOUT"
        )

    def handler_alt_shift_D(self):
        "Handles alt+shift+D, toggles decorations"

        Window.focused_window().toggle_decoration()

    def handler_alt_shift_delete(self):
        "Handles alt+shift+delete, quits the listening"
        
        #stop the polling
        self.stop = True

    def handler_alt_V(self):
        "Handles alt+V, hides taskbar"
        
        self.taskbar.toggle_visibility()

        curmonitor = Monitor.current_monitor_from_list(self.monitors)
        curmonitor.recalc_tiler_dimensions()

        self.current_tiler.tile_windows()

    def add_hotkeys_to_notifyicon(self):
        """
        Adds all the hotkeys to the notifyicon
        If you can't avoid ugly code you can do your very best to hide it :c
        """

        self.notifyicon.hotkeys.append(Hotkey(1
            , MOD_ALT
            , ord("H")
            , self.handler_alt_H))

        self.notifyicon.hotkeys.append(Hotkey(2
            , MOD_ALT
            , ord("L")
            , self.handler_alt_L))

        self.notifyicon.hotkeys.append(Hotkey(3
            , MOD_ALT
            , ord("J")
            , self.handler_alt_J))

        self.notifyicon.hotkeys.append(Hotkey(4
            , MOD_ALT
            , ord("K")
            , self.handler_alt_K))

        self.notifyicon.hotkeys.append(Hotkey(5
            , MOD_ALT
            , VK_RETURN
            , self.handler_alt_return))

        self.notifyicon.hotkeys.append(Hotkey(6
            , MOD_ALT + MOD_SHIFT
            , ord("J")
            , self.handler_alt_shift_J))

        self.notifyicon.hotkeys.append(Hotkey(7
            , MOD_ALT + MOD_SHIFT
            , ord("K")
            , self.handler_alt_shift_K))

        self.notifyicon.hotkeys.append(Hotkey(8
            , MOD_ALT + MOD_SHIFT
            , VK_RETURN
            , self.handler_alt_shift_return))

        self.notifyicon.hotkeys.append(Hotkey(9
            , MOD_ALT + MOD_SHIFT
            , ord("L")
            , self.handler_alt_shift_L))

        self.notifyicon.hotkeys.append(Hotkey(10
            , MOD_ALT + MOD_SHIFT
            , ord("H")
            , self.handler_alt_shift_H))

        self.notifyicon.hotkeys.append(Hotkey(11
            , MOD_ALT + MOD_SHIFT
            , ord("C")
            , self.handler_alt_shift_C))

        self.notifyicon.hotkeys.append(Hotkey(12
            , MOD_ALT
            , ord("1")
            , self.handler_alt_one))

        self.notifyicon.hotkeys.append(Hotkey(13
            , MOD_ALT
            , ord("2")
            , self.handler_alt_two))

        self.notifyicon.hotkeys.append(Hotkey(14
            , MOD_ALT
            , ord("3")
            , self.handler_alt_three))

        self.notifyicon.hotkeys.append(Hotkey(15
            , MOD_ALT
            , ord("4")
            , self.handler_alt_four))

        self.notifyicon.hotkeys.append(Hotkey(16
            , MOD_ALT
            , ord("5")
            , self.handler_alt_five))

        self.notifyicon.hotkeys.append(Hotkey(17
            , MOD_ALT
            , ord("6")
            , self.handler_alt_six))

        self.notifyicon.hotkeys.append(Hotkey(18
            , MOD_ALT
            , ord("7")
            , self.handler_alt_seven))

        self.notifyicon.hotkeys.append(Hotkey(19
            , MOD_ALT
            , ord("8")
            , self.handler_alt_eight))

        self.notifyicon.hotkeys.append(Hotkey(20
            , MOD_ALT
            , ord("9")
            , self.handler_alt_nine))

        self.notifyicon.hotkeys.append(Hotkey(21
            , MOD_ALT + MOD_SHIFT
            , ord("1")
            , self.handler_alt_shift_one))

        self.notifyicon.hotkeys.append(Hotkey(22
            , MOD_ALT + MOD_SHIFT
            , ord("2")
            , self.handler_alt_shift_two))

        self.notifyicon.hotkeys.append(Hotkey(23
            , MOD_ALT + MOD_SHIFT
            , ord("3")
            , self.handler_alt_shift_three))

        self.notifyicon.hotkeys.append(Hotkey(24
            , MOD_ALT + MOD_SHIFT
            , ord("4")
            , self.handler_alt_shift_four))

        self.notifyicon.hotkeys.append(Hotkey(25
            , MOD_ALT + MOD_SHIFT
            , ord("5")
            , self.handler_alt_shift_five))

        self.notifyicon.hotkeys.append(Hotkey(26
            , MOD_ALT + MOD_SHIFT
            , ord("6")
            , self.handler_alt_shift_six))

        self.notifyicon.hotkeys.append(Hotkey(27
            , MOD_ALT + MOD_SHIFT
            , ord("7")
            , self.handler_alt_shift_seven))

        self.notifyicon.hotkeys.append(Hotkey(28
            , MOD_ALT + MOD_SHIFT
            , ord("8")
            , self.handler_alt_shift_eight))

        self.notifyicon.hotkeys.append(Hotkey(29
            , MOD_ALT + MOD_SHIFT
            , ord("9")
            , self.handler_alt_shift_nine))

        self.notifyicon.hotkeys.append(Hotkey(30
            , MOD_ALT
            , ord("I")
            , self.handler_alt_I))

        self.notifyicon.hotkeys.append(Hotkey(31
            , MOD_ALT
            , ord("U")
            , self.handler_alt_U))

        self.notifyicon.hotkeys.append(Hotkey(32
            , MOD_ALT + MOD_SHIFT
            , ord("I")
            , self.handler_alt_shift_I))

        self.notifyicon.hotkeys.append(Hotkey(33
            , MOD_ALT + MOD_SHIFT
            , ord("U")
            , self.handler_alt_shift_U))

        self.notifyicon.hotkeys.append(Hotkey(34
            , MOD_ALT + MOD_SHIFT
            , ord("D")
            , self.handler_alt_shift_D))

        self.notifyicon.hotkeys.append(Hotkey(35
            , MOD_ALT
            , VK_SPACE
            , self.handler_alt_space))

        self.notifyicon.hotkeys.append(Hotkey(36
            , MOD_ALT + MOD_SHIFT
            , VK_DELETE
            , self.handler_alt_shift_delete))

        self.notifyicon.hotkeys.append(Hotkey(37
            , MOD_ALT 
            , ord("V")
            , self.handler_alt_V))
