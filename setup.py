from cx_Freeze import setup, Executable

exe = Executable(
		script = "pythonwindowstiler.py"
		,base = "Win32GUI"
        ,targetName = "PWT.exe"
        ,compress = True
        ,icon = "icons/PWT.ico"
		)

setup( 
	name = "PWT"
	,version = "0.2"
	,description = "Python Windows Tiler"
    ,author='Bob Reynders'
	,executables = [exe]
	)


