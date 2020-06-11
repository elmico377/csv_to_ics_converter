from cx_Freeze import setup, Executable

setup(name="csvToIcs", version = "1.0", description = "A tool to convert csv files to ICS", executables = [Executable("CalendarConverter.py")])
