' Double-click launcher: runs the tray app with pythonw, so no console
' window ever appears. The app goes straight to the system tray.
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = dir
sh.Run "pythonw """ & dir & "\XTrayPaste.py""", 0, False
