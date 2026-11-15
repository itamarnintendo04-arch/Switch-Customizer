# Switch Customizer by ItamarOS

Windows theme design and live preview editor for Nintendo Switch V1 and V2 concepts.

## Features (v0.1 Alpha)
- 16:9 home-screen background preview
- Artwork and music file assignment per game
- Switch V1 / V2 target selector
- Save and open JSON projects
- Windows EXE build via GitHub Actions

## Run locally
```powershell
py -m pip install -r requirements.txt
py switch_customizer.py
```

## Download Windows build
Open **Actions > Build Windows EXE > latest successful run > Artifacts** and download **SwitchCustomizer-Windows**.

## Limitations
This is a PC-only editor and preview. It does **not** modify a physical Switch, install custom firmware, install EXE apps on Switch, or play music in v0.1. Windows EXE files cannot run natively on Nintendo Switch. JSON manifests are not installable console themes. Paths to assets refer to local files.
