@echo off
setlocal ENABLEDELAYEDEXPANSION

echo Enter the name of the ssc file. (e.g. 1116.ssc)
set /P file=
for /F "delims=" %%B in ('dir /S /B "!file!"') do set source=%%B && goto :next
goto :quit

:next
if exist error_log.txt del error_log.txt

::Verify assets
ssc2museca\ssc2museca.exe -f "%source%" --verify
echo.
if %errorlevel% EQU 0 (echo   Verification success) else (echo   Verification failed.) && goto :quit

:choice
set /P c=Continue the build process? [Y/N]
if /I "%c%" EQU "Y" goto :continue
if /I "%c%" EQU "N" goto :quit
goto :choice

:continue
if not exist custom_charts Xcopy /E /I /Q /Y .\src\defaults .
ssc2museca\ssc2museca.exe -f "%source%"

:quit
cmd /k
