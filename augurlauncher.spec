# -*- mode: python -*-

block_cipher = None
dirname = os.getcwd()
a = Analysis([os.path.join(dirname, 'augurlauncher.py')],
             pathex=[os.path.join(dirname, 'augurlauncher')],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
a.datas.append(('augur.ico', os.path.join(dirname, 'augur.ico'), 'DATA'))
a.datas.append(('augur_label.png', os.path.join(dirname, 'augur_label.png'), 'DATA'))
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='augurlauncher.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon=os.path.join(dirname, 'augur.ico'))
