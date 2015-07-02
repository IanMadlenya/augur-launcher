import os
import sys
import webbrowser
import tkinter
import signal
import tkinter.ttk as ttk
import subprocess
from multiprocessing import cpu_count

if getattr(sys, "frozen", False):
    # we are running in a |PyInstaller| bundle
    BASEDIR = sys._MEIPASS
else:
    # we are running in a normal Python environment
    BASEDIR = os.path.dirname(os.path.abspath(__file__))

class AugurLauncher(object):
    CLIENT_URL = "http://client.augur.net"
    APP_DATA = os.path.join(os.path.expanduser("~"),
                            "AppData",
                            "Roaming",
                            "Augur")
    PASSWORD_FILE = os.path.join(APP_DATA, 'password.txt')
    CHAIN = os.path.join(APP_DATA, 'chain')
    BOOTNODES = [
        "enode://035b7845dfa0c0980112abdfdf4dc11087f56b77e10d2831f186ca12bc00f5b9327c427d03d9cd8106db01488905fb2200b5706f9e41c5d75885057691d9997c@[::]:30303",
        "enode://4014c7fa323dafbb1ada241b74ce16099efde03f994728a55b9ff09a9a80664920045993978de85cb7f6c2ac7e9218694554433f586c1290a8b8faa186ce072c@97.125.111.149:30303",
        "enode://587aa127c580e61a26a74ab101bb15d03e121a720401f77647d41045eae88709b01136e30aba56d1feddff757d4a333f68b9a749acd6852f20ba16ef6e19855a@[::]:30303",
        "enode://21f857e6a74af94c47671bbd380bef3b88c246933cfa0a7f17902bc62e66ac9e98ba57130043aa155779e6c8e70957d291fc74cf1a320c8ac262af228a101206@73.189.126.112:30303",
        "enode://e30a4cd1ec5ca4dbd19c40785d7d61363b44110cb20f27a21c5009ec20f68548b1d0705ba4483cb889cf835e0774db4df0f062054b412b0e17dae063c875939e@[::]:30303",
        "enode://421e3c654f6d18559b4624eafa00d8976f7e91113c6d549c9782de0552c25300ab2e127d45e134c63ffd7c7fe1da0a0f421dbeb87ed227abf6d660dd630c315e@24.4.140.216:30303",
    ]
    GETH_COMMAND = [
            "C:\\Program Files\\Augur\\geth.exe",
            "--password", PASSWORD_FILE,
            "--unlock", "primary",
            "--datadir", CHAIN,
            "--shh",
            "--rpc",
            "--rpccorsdomain", "http://client.augur.net",
            "--genesisnonce", "1010101",
            "--networkid", "1010101",
            "--bootnodes", " ".join(BOOTNODES)]
    GETH_MINE_COMMAND = GETH_COMMAND + ["--mine",
                                        "--minerthreads", str(cpu_count())]
    
    def __init__(self):
        self.master = tkinter.Tk()
        self.master.resizable(0, 0)
        self.master.title("Augur Launcher")
        self.master.iconbitmap(os.path.join(
            BASEDIR,
            "augur.ico"))
        
        self.style = ttk.Style()
        self.style.configure("TButton", background="#5f2150")

        self.top_frame = tkinter.Frame(self.master, background="#5f2150")
        self.top_frame.pack(fill="both", expand=True)

        self.logo_image = tkinter.PhotoImage(file=os.path.join(
            BASEDIR,
            'augur_label.png'))
        self.logo_label = tkinter.Label(self.top_frame,
                                        image=self.logo_image,
                                        background="#5f2150")
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.button_frame = tkinter.Frame(self.top_frame, background="#5f2150")
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
