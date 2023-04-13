import os
import subprocess
import platform
from reapy_boost import reascript_api as RPR

def find_python_path():
    python_paths = ["/usr/local/bin/python", "/usr/bin/python"]
    for path in python_paths:
        if os.path.exists(path):
            return path
    return None

reaper_scripts_path = os.path.join(RPR.GetResourcePath(), "Scripts")
bezier2env_main_path = os.path.join(reaper_scripts_path, "bezier2env_main.py")

if platform.system() == "Windows":
    python_command = None
    paths = os.environ["PATH"].split(";")
    for p in paths:
        file_path = os.path.join(p, "python.exe")
        if os.path.exists(file_path):
            python_command = file_path
            break
else:
    python_command = find_python_path()

if not python_command:
    RPR.ShowMessageBox("Python not found in the system PATH.", "Error", 0)
    sys.exit()

command = f"{python_command} \"{bezier2env_main_path}\""

if platform.system() == "Windows":
    cmd = f"start \"\" cmd.exe /C cd \"{reaper_scripts_path}\" && {command}"
else:
    cmd = f"{command} &"

subprocess.Popen(cmd, shell=True)

