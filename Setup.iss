; Build with Inno Setup Compiler 6.2.2

[Setup]
DisableDirPage=yes
AppName=XISO Toolkit
AppVersion=0.1
WizardStyle=modern
DefaultDirName=C:\XISOTools\
DefaultGroupName=XISOTools
UninstallDisplayIcon={app}\Uninstall.exe
Compression=lzma2
SolidCompression=yes
OutputDir=userdocs:Inno Setup Examples Output
DisableProgramGroupPage=yes
AllowNoIcons=yes
CreateUninstallRegKey=yes
//LicenseFile=License.txt



[Code]
var
  WelcomePage: TWizardPage;

procedure InitializeWizard;
begin
  WelcomePage := CreateCustomPage(wpWelcome, 'Welcome', 'IDK how to customize this.' + #13#10 + 'Click Next to continue with the installation.'+ #13#10 +'This text will be cut off..');
end;


[Files]
Source: "C:\XISOTools\build.exe"; DestDir: "{app}"
Source: "C:\XISOTools\Split.exe"; DestDir: "{app}"
Source: "C:\XISOTools\xbedump.exe"; DestDir: "{app}"
Source: "C:\XISOTools\icons\*"; DestDir: "{app}\icons"; Flags: recursesubdirs createallsubdirs
Source: "C:\XISOTools\music\*"; DestDir: "{app}\music"; Flags: recursesubdirs createallsubdirs

[Dirs]
Name: "{app}\tmp"; Permissions: users-modify

[Registry]
Root: HKCR; Subkey: "*\shell\XISO Tools"; ValueType: string; ValueName: "MUIVerb"; ValueData: "XISO Tools"
Root: HKCR; Subkey: "*\shell\XISO Tools"; ValueType: string; ValueName: "SubCommands"; ValueData: ""
Root: HKCR; Subkey: "*\shell\XISO Tools"; ValueType: string; ValueName: "AppliesTo"; ValueData: ".iso"
Root: HKCR; Subkey: "*\shell\XISO Tools"; ValueType: string; ValueName: "Icon"; ValueData: "C:\XISOTools\icons\xios.ico"

Root: HKCR; Subkey: "*\shell\XISO Tools\shell"; Flags: uninsdeletekeyifempty

Root: HKCR; Subkey: "*\shell\XISO Tools\shell\01menu"; ValueType: string; ValueName: "AppliesTo"; ValueData: ".iso"
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\01menu"; ValueType: string; ValueName: "MUIVerb"; ValueData: "Build attacher"
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\01menu"; ValueType: string; ValueName: "Icon"; ValueData: "C:\XISOTools\icons\xbe.ico"
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\01menu\command"; ValueType: string; ValueName: ""; ValueData: "C:\XISOTools\build.exe ""%1"""

Root: HKCR; Subkey: "*\shell\XISO Tools\shell\02menu"; ValueType: string; ValueName: "AppliesTo"; ValueData: ".iso"
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\02menu"; ValueType: string; ValueName: "MUIVerb"; ValueData: "Split large XISO"
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\02menu"; ValueType: string; ValueName: "Icon"; ValueData: "C:\XISOTools\icons\split.ico"
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\02menu\command"; ValueType: string; ValueName: ""; ValueData: "C:\XISOTools\Split.exe ""%1"""

Root: HKCR; Subkey: "*\shell\XISO Tools\shell\03menu"; ValueType: string; ValueName: "AppliesTo"; ValueData: ".iso"
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\03menu"; ValueType: string; ValueName: "MUIVerb"; ValueData: "Rebuild Redump into XISO"
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\03menu"; ValueType: string; ValueName: "Icon"; ValueData: "C:\XISOTools\icons\redump.ico"
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\03menu\command"; ValueType: string; ValueName: ""; ValueData: """C:\XISOTools\extract-xiso.exe"" -r -D ""%1\"""

;Uninstall
;Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{AppId}"; ValueType: string; ValueName: "DisplayName"; ValueData: "{AppName}"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools"; ValueType: string; ValueName: "MUIVerb"; ValueData: "XISO Tools"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools"; ValueType: string; ValueName: "SubCommands"; ValueData: ""; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools"; ValueType: string; ValueName: "AppliesTo"; ValueData: ".iso"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icons\xios.ico"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\01menu"; ValueType: string; ValueName: "AppliesTo"; ValueData: ".iso"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\01menu"; ValueType: string; ValueName: "MUIVerb"; ValueData: "Build attacher"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\01menu"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icons\xbe.ico"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\01menu\command"; ValueType: string; ValueData: """{app}\build.exe"" ""%1"""; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\02menu"; ValueType: string; ValueName: "AppliesTo"; ValueData: ".iso"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\02menu"; ValueType: string; ValueName: "MUIVerb"; ValueData: "Split large XISO"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\02menu"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icons\split.ico"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\02menu\command"; ValueType: string; ValueData: """{app}\Split.exe"" ""%1"""; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\03menu"; ValueType: string; ValueName: "AppliesTo"; ValueData: ".iso"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\03menu"; ValueType: string; ValueName: "MUIVerb"; ValueData: "Rebuild Redump into XISO"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\XISO Tools\shell\03menu"; ValueType: string; ValueName:







