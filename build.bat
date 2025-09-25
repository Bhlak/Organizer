@echo off
pyinstaller --noconfirm ^
  --distpath "P:\Organizer\builds\release" ^
  --workpath "P:\Organizer\builds\tmp" ^
  --clean app_build.spec
