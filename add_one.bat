@echo off
cd /d %~dp0

if [%1] equ [] (echo Drag and drop a chart folder onto this file. && goto :quit) else (
  for /F "delims=" %%B in ('dir /S /B "%~1\*.ssc"') do set source="%%B"
  goto :next
)

:next
ssc2museca\ssc2museca.exe -f %source%

:quit
echo.
cmd /k
