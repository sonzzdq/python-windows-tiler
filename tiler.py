import ctypes
import windowutilities

from win32con import SPI_GETWORKAREA

class Tiler:

    def __init__(self):

        class Crect(ctypes.Structure):
            _fields_ = [('left', ctypes.c_ulong),
                    ('top', ctypes.c_ulong),
                    ('right', ctypes.c_ulong),
                    ('bottom', ctypes.c_ulong)]

        r = Crect()

        ctypes.windll.user32.SystemParametersInfoA(SPI_GETWORKAREA, 0, ctypes.byref(r), 0)

        self.width = r.right - r.left
        self.height = r.bottom - r.top

        self.masterareaWidth = self.width // 2
        self.masterareaSize = 1

    def tile_windows(self, windows=None):
        "Tiles all windows, if windows are given it sets them to the self.windows attribute"

        if windows is not None:

            self.windows = windows

        if len(self.windows) > 1:

            if self.masterareaSize == len(self.windows):

                height = self.height

            else:

                height = self.height // (len(self.windows) - self.masterareaSize)

            if self.masterareaSize >= len(self.windows):

                heightMaster = self.height // len(self.windows)
                width = self.width

            else:

                heightMaster = self.height // self.masterareaSize
                width = self.masterareaWidth

            for i, window in enumerate(self.windows):

                if i in range(self.masterareaSize):

                    rectangleCoordinates = (0,i * heightMaster, width, (i + 1) * heightMaster)

                else:

                    rectangleCoordinates = (width, (i - self.masterareaSize) * height, self.width, (i - self.masterareaSize + 1) * height)

                windowutilities.tile(window, rectangleCoordinates)

        elif len(self.windows) > 0:

            windowutilities.tile(self.windows[0], (0, 0, self.width, self.height))
