from cx_Freeze import setup, Executable
import sys
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["tkinter", "unittest"],
    "zip_include_packages": ["encodings", "PySide6", "shiboken6"],
    "packages" : ["pyttsx3"]
}
base = "Win32GUI" if sys.platform == "win32" else None
setup(
    name="Jarvis 2.o",
    version="2.0",
    description="Mera Pyara Jarvis",
    options={"build_exe": build_exe_options},
    executables=[Executable("jarvis_main.py", base=base)],
)