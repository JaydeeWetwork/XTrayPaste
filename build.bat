@echo off
rem Build XTrayPaste.exe - one file, no console window, X icon.
rem Needs: pip install pystray Pillow keyboard pyinstaller

python -c "from PIL import Image, ImageDraw; img = Image.new('RGBA', (64, 64), (0, 0, 0, 255)); d = ImageDraw.Draw(img); d.line([(12, 12), (52, 52)], fill=(255, 255, 255, 255), width=8); d.line([(52, 12), (12, 52)], fill=(255, 255, 255, 255), width=8); img.save('x-icon.ico', sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)])"
pyinstaller --onefile --noconsole --icon x-icon.ico --name XTrayPaste XTrayPaste.py
echo.
echo Built: dist\XTrayPaste.exe
pause
