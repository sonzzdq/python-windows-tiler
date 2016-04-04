#This page will teach you the basics of the config file.

# Config file #

The default config file currently has 3 sections, global, hotkey and window.

## Global ##

Center\_cursor expects a boolean value to either enable or disable the feature.

  * center\_cursor = yes

## Hotkey ##

The hotkey value expects the form of < modifier+modifier.. >+< key >. [Possible keys](http://code.google.com/p/python-windows-tiler/source/browse/pwt/hotkey.py)

  * remove\_window\_from\_master = alt+shift+l
  * add\_window\_to\_master = alt+shift+h
  * focus\_next\_window = alt+j
  * focus\_previous\_window = alt+k
  * focus\_primary\_window = alt+return
  * shift\_focused\_window\_down = alt+shift+j
  * shift\_focused\_window\_up = alt+shift+k
  * shift\_focused\_window\_to\_primary = alt+shift+return
  * decrease\_master\_size = alt+h
  * increase\_master\_size = alt+l
  * close\_focused\_window = alt+shift+c
  * switch\_to\_group\_1 = alt+1
  * switch\_to\_group\_2 = alt+2
  * switch\_to\_group\_3 = alt+3
  * switch\_to\_group\_4 = alt+4
  * switch\_to\_group\_5 = alt+5
  * switch\_to\_group\_6 = alt+6
  * switch\_to\_group\_7 = alt+7
  * switch\_to\_group\_8 = alt+8
  * switch\_to\_group\_9 = alt+9
  * send\_to\_group\_1 = alt+shift+1
  * send\_to\_group\_2 = alt+shift+2
  * send\_to\_group\_3 = alt+shift+3
  * send\_to\_group\_4 = alt+shift+4
  * send\_to\_group\_5 = alt+shift+5
  * send\_to\_group\_6 = alt+shift+6
  * send\_to\_group\_7 = alt+shift+7
  * send\_to\_group\_8 = alt+shift+8
  * send\_to\_group\_9 = alt+shift+9
  * focus\_next\_monitor = alt+i
  * focus\_previous\_monitor = alt+u
  * shift\_to\_next\_monitor = alt+shift+i
  * shift\_to\_previous\_monitor = alt+shift+u
  * choose\_next\_layout = alt+space
  * toggle\_focused\_window\_decoration = alt+shift+d
  * stop\_pythonwindowstiler = alt+shift+delete
  * toggle\_taskbar\_visibility = alt+v
  * print\_focused\_window\_classname = alt+s
  * tile\_focused\_window = alt+t
  * float\_focused\_window = alt+shift+t

## Window ##

Window holds the window rules, currently there are 2 rules defined, float and decorate. Due to the nature of some apps they struggle with being tiled. Forcing the decorations on can help get rid of some of the glitches, if that doesn't help you can force float them. If a window gets tiled that shouldn't get tiled you should also add it to float.

The expected format is < window classname >;< window classname >

  * float = `progman;#32770`
  * decorate = `Chrome_WidgetWin_0;ConsoleWindowClass`

## Example ##

You can remove keybinds from the config to ignore the entire function as I do in my [own config file](http://sourcetumble.appspot.com/my-config-file/).