; Installeur Windows de PDF DUO (Inno Setup 6)
#ifndef MyVersion
  #define MyVersion "1.0.0"
#endif
[Setup]
AppId={{6E2B3C1A-7F4D-4C2B-9A51-5D0F1E2A4D50}
AppName=PDF DUO
AppVersion={#MyVersion}
AppPublisher=Jacques Branas
AppPublisherURL=https://deltapassion.github.io/PDF-DUO/
AppSupportURL=https://github.com/Deltapassion/PDF-DUO/issues
DefaultDirName={autopf}\PDF DUO
DefaultGroupName=PDF DUO
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
OutputDir=Output
OutputBaseFilename=PDF-DUO-Windows-Setup
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\PDF DUO.exe
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "pt"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "it"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "el"; MessagesFile: "Greek.isl"
Name: "zh"; MessagesFile: "ChineseSimplified.isl"
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "uk"; MessagesFile: "compiler:Languages\Ukrainian.isl"
Name: "ar"; MessagesFile: "Arabic.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "pdfassoc"; Description: "PDF → PDF DUO"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\PDF DUO\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\PDF DUO"; Filename: "{app}\PDF DUO.exe"
Name: "{group}\{cm:UninstallProgram,PDF DUO}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\PDF DUO"; Filename: "{app}\PDF DUO.exe"; Tasks: desktopicon

[Registry]
Root: HKA; Subkey: "Software\Classes\PDFDUO.pdf"; ValueType: string; ValueName: ""; ValueData: "Document PDF (PDF DUO)"; Flags: uninsdeletekey; Tasks: pdfassoc
Root: HKA; Subkey: "Software\Classes\PDFDUO.pdf\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\PDF DUO.exe"" ""%1"""; Tasks: pdfassoc
Root: HKA; Subkey: "Software\Classes\.pdf\OpenWithProgids"; ValueType: string; ValueName: "PDFDUO.pdf"; ValueData: ""; Flags: uninsdeletevalue; Tasks: pdfassoc

[INI]
; langue choisie dans l'installeur : PDF DUO démarre directement dans cette langue
Filename: "{app}\langue.ini"; Section: "PDF DUO"; Key: "langue"; String: "{language}"

[UninstallDelete]
Type: files; Name: "{app}\langue.ini"

[Run]
Filename: "{app}\PDF DUO.exe"; Description: "{cm:LaunchProgram,PDF DUO}"; Flags: nowait postinstall skipifsilent
