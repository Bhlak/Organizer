@echo off
pyinstaller --noconfirm ^
  --distpath "P:\Developed\Organizer\builds\release" ^
  --workpath "P:\Developed\Organizer\builds\tmp" ^
  --clean app_build.spec
