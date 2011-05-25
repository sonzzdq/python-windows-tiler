from cx_Freeze import setup, Executable

exe = Executable(
		script = "pythonwindowstiler.py"
		,base = "Win32GUI"
        ,targetName = "PWT.exe"
        ,compress = True
        ,icon = "PWT.ico"
		)

setup( 
	name = "PWT"
	,version = "0.2"
	,description = "Python Windows Tiler V0.2"
    ,author='Bob Reynders'
	,executables = [exe]
	)


