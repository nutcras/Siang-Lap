@echo off
echo ========================
echo Killing any running SiangLap.exe...
taskkill /f /im SiangLap.exe 2>nul

echo ========================
echo Cleaning old build folders...
rmdir /s /q build
rmdir /s /q dist

echo ========================
echo Building with PyInstaller...
pyinstaller --clean --noconfirm SiangLap.spec

echo ========================
echo Build finished!
pause