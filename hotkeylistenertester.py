import hotkeylistener

from win32con import MOD_ALT

def print_windows(windows):
	for window in windows:
		print(window)

def handler_alt_Y():
	print("This shit is working YE")

if __name__ == "__main__":

	hotkeys = {1: (MOD_ALT, ord("Y"))
			}

	hotkeyhandlers = {1: handler_alt_Y
			}

	listener = hotkeylistener.HotkeyListener(hotkeys, hotkeyhandlers)
	listener.listen_to_hotkeys()
