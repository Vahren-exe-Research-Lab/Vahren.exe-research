@echo off
rem 研究資料の目録を作る（knowledge\CATALOG.md）。ダブルクリックで実行
cd /d "%~dp0..\.."
set PYTHONUTF8=1
where py >nul 2>nul
if %errorlevel%==0 (py -3 -B knowledge\tools\build_catalog.py) else (python -B knowledge\tools\build_catalog.py)
echo.
pause
