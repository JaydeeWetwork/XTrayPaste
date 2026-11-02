# X Tray Paste

A tiny Windows tray app with one job: press **Alt+X** anywhere and the X symbol (𝕏) is typed straight into the active input box. **Hold Alt+X down and it keeps typing**, like holding any other key.

The symbol never travels through the clipboard. It is sent as keystrokes, so there is no copy step, no paste delay, and your clipboard is never touched or overwritten. The only timing anywhere in the app is the repeat cadence while the keys are held: one symbol about every 35 ms.

- **Icon:** an X, sitting in your system tray
- **Window:** none. No console, no window, ever. Click it and it goes straight to the tray.
- **Symbol:** 𝕏, Unicode U+1D54F MATHEMATICAL DOUBLE-STRUCK CAPITAL X, the same character the X logo uses

## Quick start (the exe, no Python needed)

1. Open this repo's **Actions** tab.
2. Click the latest **Build Windows exe** run.
3. Scroll to **Artifacts** and download **XTrayPaste-exe**. Unzip it.
4. Double-click **XTrayPaste.exe**. Nothing visible happens, and that is correct: look in your system tray (the icons near the clock, click the little **^** arrow if you do not see it) and the X icon is there.
5. Click into any text box anywhere, press **Alt+X**, and 𝕏 appears. Hold it down for a stream of them.

## Running from the Python script

Use this route if you want to read or tinker with the code, or if the exe is not built yet.

**You need:** Windows, and Python 3.10 or newer from python.org. During the Python install, tick the box that says **Add python.exe to PATH**... without it the commands below will not find Python.

1. Download this repo (green **Code** button, **Download ZIP**) and unzip it, or clone it with git.
2. Open a terminal in the unzipped folder (right-click inside the folder, **Open in Terminal**).
3. Install the three small libraries it uses:
   ```
   pip install -r requirements.txt
   ```
4. Start it:
   ```
   python XTrayPaste.py
   ```
   That route shows a console window while it runs. If you want **no console window**, double-click **XTrayPaste.vbs** instead: it launches the app with `pythonw`, and it goes straight to the tray.

## The tray menu

Right-click the X icon in the tray:

- **Copy X to clipboard** ... puts 𝕏 on your clipboard without typing it, handy if you want to paste it several places by hand with Ctrl+V.
- **Quit** ... closes the app completely. The icon disappears and Alt+X goes back to doing nothing.

## Run it at startup

1. Press **Win+R**, type `shell:startup`, and press Enter. A folder opens.
2. Drop **XTrayPaste.exe** (or a shortcut to it, or a shortcut to **XTrayPaste.vbs**) into that folder.
3. Done. It will start silently in the tray every time you log in. To stop that, just remove it from the same folder.

## Build the exe yourself

- Install the script dependencies plus PyInstaller:
  ```
  pip install pystray Pillow keyboard pyinstaller
  ```
- Double-click **build.bat**. It draws the X icon file and then builds the app. The result lands in `dist\XTrayPaste.exe`: a single self-contained file, no console window, with the X as its icon.
- Every push to this repo also builds the exe automatically: see the **Actions** tab.

## How it works

- `keyboard` registers one global hotkey, **Alt+X**, with suppression, so the app underneath never sees a stray Alt+X menu shortcut.
- On the press, the symbol is typed with `keyboard.write`, which sends it as Unicode keystroke events. Nothing is copied, nothing is pasted.
- While both keys stay down, a small loop keeps typing every 35 ms and stops the moment either key comes up.
- `pystray` owns the tray icon and its menu. The icon is drawn at runtime with Pillow: two bold white strokes on black, no image files needed.
- The one clipboard feature, **Copy X to clipboard**, writes the symbol through the plain Windows API (`SetClipboardData`), so the app needs no clipboard library at all.

## Troubleshooting

- **Alt+X does nothing in one specific app, but works elsewhere.** That app is probably running as administrator. Windows will not let a normal app send keystrokes into an elevated one. Run XTrayPaste as administrator too, or run that app unelevated.
- **Nothing happens anywhere.** Check the tray: if the X icon is not there, the app is not running. Start it again. If the icon is there, make sure no other program has claimed Alt+X globally.
- **The exe gets flagged or blocked on first run.** Fresh PyInstaller builds sometimes trip cautious antivirus heuristics. Building it yourself with `build.bat`, or running the Python script route, sidesteps that entirely... the full source is right here to read first.
- **You held the keys and got a flood.** That is the repeat working as designed. Let go sooner, or raise `REPEAT_SECONDS` in `XTrayPaste.py` for a slower stream.

## Files

- `XTrayPaste.py` ... the whole app, one file
- `XTrayPaste.vbs` ... double-click launcher with no console window
- `build.bat` ... builds `XTrayPaste.exe` locally
- `requirements.txt` ... the script's three libraries (pystray, Pillow, keyboard)
- `.github/workflows/build.yml` ... builds the exe on a Windows runner for every push
