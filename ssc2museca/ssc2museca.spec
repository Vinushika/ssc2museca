# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ssc2museca.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=["jinxed.terminfo.vtwin10", "enlighten", "chartv2", "ssc2museca.chartv2"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ssc2museca',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
