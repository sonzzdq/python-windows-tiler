from pwt.controller import Controller
from singleinstance import singleinstance
import sys

if __name__ == "__main__":

    #way to assure a singleinstance
    this = singleinstance()

    if not this.alreadyrunning():

        #initialization

        controller = Controller()

        controller.start()

