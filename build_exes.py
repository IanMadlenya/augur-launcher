import os
import shutil
import traceback
import subprocess

#assumes you have the pyinstaller repo in the same
#directory as the augur-launcher repo.
CWD = os.getcwd()
DIRNAME = os.path.dirname(CWD)
PYINSTALLER = os.path.join(DIRNAME,
                           "pyinstaller",
                           "pyinstaller.py")

def build_clean(name):
    subprocess.check_output(["python",
                             PYINSTALLER,
                             name + ".spec"])
    shutil.copy(os.path.join("dist",
                             name + ".exe"),
                CWD)
    shutil.rmtree("build")
    shutil.rmtree("dist")

def main():
    for name in ("augurlauncher", "Augur Installer"):
        build_clean(name)

    os.system("pause")

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        os.system("pause")
