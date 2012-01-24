import os.path
import configparser

config = configparser.ConfigParser()

if os.path.isfile("config.ini"):

    config.read("config.ini")

else:

    config["global"] = {
            "center_cursor" : "yes"
    }

    config["window"] = {
            "float" : "progman;#32770"
            , "decorate" : "Chrome_WidgetWin_0;ConsoleWindowClass"
    }

    with open("config.ini", "w") as configfile:
        config.write(configfile)
