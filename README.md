# augur-launcher
Python source for the client launcher and installer.

### Building the binaries
To get the binaries, you can download them ~~here~~. <br><br>
If you really want to build the binaries on Windows, you need to have [python 3](https://www.python.org/downloads/windows/) installed (it helps to add python.exe to your path, which is an option in the installer), and you need to use the python 3 branch of [pyinstaller](https://github.com/pyinstaller/pyinstaller/tree/python3). You will also need to install the correct version of [pywin32](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/). Then, open a command prompt and enter
```
cd C:\path\to\augur-launcher
python C:\path\to\pyinstaller.py augur_launcher.spec
python C:\path\to\pyinstaller.py "Augur Installer.spec"
```
To update the version of geth used in the installer, simply copy the geth binary into the repo. You don't need to rebuild the launcher to change the geth version, just build `Augur Installer.exe`
