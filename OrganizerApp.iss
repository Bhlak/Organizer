; Inno Setup Script for OrganizerApp

[Setup]
AppName=OrganizerApp
AppVersion=1.0
AppPublisher=Your Name or Company
AppPublisherURL=http://example.com
DefaultDirName={pf}\OrganizerApp
DefaultGroupName=OrganizerApp
UninstallDisplayIcon={app}\Organizer.exe
Compression=lzma
SolidCompression=yes
OutputBaseFilename=OrganizerApp-Setup
OutputDir=.\builds\installer
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Copy everything from your PyInstaller dist folder
Source: "P:\Developed\Organizer\builds\release\OrganizerApp\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
; Start Menu
Name: "{group}\Organizer"; Filename: "{app}\Organizer.exe"
Name: "{group}\Uninstall OrganizerApp"; Filename: "{uninstallexe}"

; Desktop shortcut
Name: "{commondesktop}\Organizer"; Filename: "{app}\Organizer.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
; Optionally run the app after install
Filename: "{app}\Organizer.exe"; Description: "Launch Organizer"; Flags: nowait postinstall skipifsilent
