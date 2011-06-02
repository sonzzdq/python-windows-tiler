from cx_Freeze import setup, Executable

exe = Executable(
		script = "pwt.py"
		,base = "Win32GUI"
        ,targetName = "PWT.exe"
        ,compress = True
        ,icon = "icons/PWT.ico"
		)

setup( 
	name = "PWT"
	,version = "0.6"
	,description = "Python Windows Tiler"
    ,author="Bob Reynders"
	,executables = [exe]
	)


