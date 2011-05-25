import windowlistener

def print_windows(windows):
	for window in windows:
		print(window)

if __name__ == "__main__":
	listener = windowlistener.WindowListener([])
	listener.listen_to_windows(print_windows)

