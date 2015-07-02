# -*- mode: python -*-

block_cipher = None
dirname = os.getcwd()

a = Analysis([os.path.join(dirname, 'Augur Installer.py')],
             pathex=[os.path.join(dirname, 'Augur Installer')],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)

a.datas.append(('augurlauncher.exe', os.path.join(dirname, 'augurlauncher.exe'), 'DATA'))
a.datas.append(('geth.exe', os.path.join(dirname, 'geth.exe'), 'DATA'))

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Augur Installer.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , uac_admin=True, icon='C:\\Users\\Chris\\Desktop\\augur\\augur.ico')
