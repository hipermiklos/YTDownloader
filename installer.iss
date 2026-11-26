#define AppName "Hipermiklos YTDownloader"
#define AppVersion "1.0.0"
#define AppExeName "Hipermiklos_YTDownloader.exe"

[Setup]
AppId={{A7A02304-8E13-4F80-91A0-35D88FB0A2EF}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Hipermiklos Softwares
DefaultDirName={autopf}\Hipermiklos_Softwares\YTDownloader
DefaultGroupName={#AppName}
OutputDir=dist\installer
OutputBaseFilename=Hipermiklos_YTDownloader_Setup
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#AppExeName}
SetupIconFile=icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "dist\release\Hipermiklos_YTDownloader\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: postinstall nowait skipifsilent
