# augur-launcher
Python source for the Windows (64 bit only!) client launcher and installer.

### Building the binaries
To get the installer, you can download it ~~here~~. <br><br>
If you really want to build the binaries on Windows, you need to have [python 3](https://www.python.org/downloads/windows/) installed (it helps to add python.exe to your path, which is an option in the installer.) You will also need to use the python 3 branch of [pyinstaller](https://github.com/pyinstaller/pyinstaller/tree/python3). Make sure that the pyinstaller folder is in the same directory as the augur-launcher folder. The last dependency is [pywin32](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/). Once you've got all the dependencies, double click build_exes.py and it should build the binaries.<br>
To update the version of geth used in the installer, simply copy the new geth binary into the repo, and run the build script.
