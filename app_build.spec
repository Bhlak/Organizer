from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, MERGE

hidden = collect_submodules("win32com")

datas = [
    ("convenient.py", "."),
    ("defaults/*", "defaults"),
    ("defaults/schedule.json", "defaults"),
    ("defaults/folders.txt", "defaults"),
]


a1 = Analysis(
    ['gui.py'],
    pathex=['.'],
    hiddenimports=hidden,
    datas=datas,
    binaries=[],
    noarchive=False,
)
pyz1 = PYZ(a1.pure, a1.zipped_data, cipher=None)
exe1 = EXE(
    pyz1,
    a1.scripts,
    [],
    exclude_binaries=True,
    name='Organizer',
    console=False,
)

a2 = Analysis(
    ['executor.py'],
    pathex=['.'],
    hiddenimports=hidden,
    datas=datas,
    binaries=[],
    noarchive=False,
)
pyz2 = PYZ(a2.pure, a2.zipped_data, cipher=None)
exe2 = EXE(
    pyz2,
    a2.scripts,
    [],
    exclude_binaries=True,
    name='Executor',
    console=False,
)

coll = COLLECT(
    exe1,
    exe2,
    a1.binaries + a2.binaries,
    a1.datas + a2.datas,
    name="OrganizerApp",
    strip=False,
    upx=True,
    upx_exclude=[],
)