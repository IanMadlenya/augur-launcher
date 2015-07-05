import os
import sys
import shutil
import binascii
import traceback
import subprocess
from win32com.client import Dispatch

LAUNCHER_PATH = "C:\\Program Files\\Augur"
DATA_PATH = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', "Augur")
PASSFILE = os.path.join(DATA_PATH, "password.txt")

if getattr(sys, 'frozen', False):
    # we are running in a |PyInstaller| bundle
    BASEDIR = sys._MEIPASS
else:
    # we are running in a normal Python environment
    BASEDIR = os.path.dirname(os.path.abspath(__file__))

GETH_EXE = os.path.join(BASEDIR, 'geth.exe')
LAUNCHER_EXE = os.path.join(BASEDIR, 'augurlauncher.exe')

def main():
    # first make all the appropriate directories
    print("Making directories...")
    for d in LAUNCHER_PATH, DATA_PATH:
        print("Creating", d, end=" ", flush=True)
        os.mkdir(d)
        print("Success!")

    print("Generating random password file...", end=" ", flush=True)
    # then generate the password
    password = binascii.b2a_hex(os.urandom(32))
    passfile = open(PASSFILE, "w")
    passfile.write(password.decode('ascii'))
    passfile.close()
    print("Success!")

    # Then copy ".exe"s to the launcher path
    exes = GETH_EXE, LAUNCHER_EXE
    results = []
    for exe in exes:
        print("Copying", os.path.basename(exe), "to", LAUNCHER_PATH, "...", end=" ", flush=True)
        results.append(shutil.copy(exe, LAUNCHER_PATH))
        print("Sucess!")

    print("Creating node account...", end=" ", flush=True)
    # create account on node
    p = subprocess.Popen([results[0],
                      "--password", PASSFILE,
                      "account", "new"])
    p.wait()
    print("Success!")

    print("Creating shortcut...", end=" ", flush=True)
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    shortcut_path = os.path.join(desktop, "Augur Launcher.lnk")
    wDir = LAUNCHER_PATH

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = results[1]
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = results[1]
    shortcut.save()
    print("Success!")

def uninstall():
    paths = LAUNCHER_PATH, DATA_PATH
    for p in paths:
        print("Deleting", p, "...", end=" ", flush=True)
        shutil.rmtree(p)
        print("Success!")
    print("Removing desktop shortcut...", end=" ", flush=True)
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    shortcut_path = os.path.join(desktop, "Augur Launcher.lnk")
    os.remove(shortcut_path)
    print("Success!")

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2 and sys.argv[1] == 'uninstall':
            uninstall()
        elif len(sys.argv) == 1:
            main()
        else:
            assert len(sys.argv) <= 2, "wrong number of arguements!"
    except Exception as exc:
        traceback.print_exc()
    finally:
        os.system("pause")
        sys.exit(0)
