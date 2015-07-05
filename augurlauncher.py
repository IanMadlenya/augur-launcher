import os
import sys
import webbrowser
import tkinter
import signal
import tkinter.ttk as ttk
import subprocess
from multiprocessing import cpu_count

class AugurLauncher(object):
    if getattr(sys, "frozen", False):
        # we are running in a |PyInstaller| bundle
        BASEDIR = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        BASEDIR = os.path.dirname(os.path.abspath(__file__))
    CLIENT_URL = "http://client.augur.net"
    PASSWORD_FILE = os.path.join(
        os.path.expanduser("~"),
        "AppData",
        "Roaming",
        "Augur",
        "password.txt")
    GETH_COMMAND = [
        "C:\\Program Files\\Augur\\geth.exe",
        "--password", PASSWORD_FILE,
        "--unlock", "0",
        "--shh",
        "--rpc",
        "--rpccorsdomain", "http://client.augur.net",
        ]
    GETH_MINE_COMMAND = GETH_COMMAND + ["--mine",
                                        "--minerthreads", str(cpu_count())]
    PURPLE = "#5f2150"
    def __init__(self):
        self.master = tkinter.Tk()
        self.master.resizable(0, 0)
        self.master.title("Augur Launcher")
        self.master.iconbitmap(os.path.join(
            self.BASEDIR,
            "augur.ico"))
        
        self.style = ttk.Style()
        self.style.configure("TButton", background=self.PURPLE)

        self.top_frame = tkinter.Frame(self.master, background=self.PURPLE)
        self.top_frame.pack(fill="both", expand=True)

        self.logo_image = tkinter.PhotoImage(file=os.path.join(
            self.BASEDIR,
            'augur_label.png'))
        self.logo_label = tkinter.Label(self.top_frame,
                                        image=self.logo_image,
                                        background=self.PURPLE)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.button_frame = tkinter.Frame(self.top_frame, background=self.PURPLE)
        self.button_frame.grid(row=0, column=1)
        self.open_client = ttk.Button(self.button_frame,
                                      style='TButton',
                                      text="Launch Client",
                                      command=self.open_client_command)
        self.open_client.grid(row=0, column=0,
                              ipadx=10, ipady=10,
                              pady=10, padx=10,
                              sticky='w')

        self.miner_state = tkinter.IntVar()
        self.miner_state.set(0)
        self.enable_miner = ttk.Checkbutton(self.button_frame,
                                            text="Enable Mining",
                                            command=self.toggle_miner,
                                            variable=self.miner_state)
        self.enable_miner.grid(row=1, column=0)
        self.geth = subprocess.Popen(self.GETH_COMMAND,
                                     stdout=subprocess.PIPE,
                                     creationflags=512) #yay for magic!
                                                        #needed for signal
                                                        #to work properly.
        
    def mainloop(self):
        self.master.mainloop()

    def open_client_command(self):
        webbrowser.open(self.CLIENT_URL)

    def toggle_miner(self):
        self.geth.send_signal(signal.CTRL_BREAK_EVENT)
        self.geth.wait()
        if self.miner_state.get():
            self.geth = subprocess.Popen(self.GETH_MINE_COMMAND,
                                         stdout=subprocess.PIPE,
                                         creationflags=512)
        else:
            self.geth = subprocess.Popen(self.GETH_COMMAND,
                                         stdout=subprocess.PIPE,
                                         creationflags=512)
if __name__ == '__main__':
    app = AugurLauncher()
    app.mainloop()
    app.geth.send_signal(signal.CTRL_BREAK_EVENT)
