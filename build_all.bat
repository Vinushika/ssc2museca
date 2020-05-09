@echo off
setlocal ENABLEDELAYEDEXPANSION

set source=".\src\custom_charts"

if exist error_log.txt del error_log.txt

set error=0

::Verify assets
ssc2museca\ssc2museca.exe --verify
if %errorlevel% EQU 1 (set /a error=1)
if %error% EQU 0 (echo   Verification success) else (echo   Verification failed.) && goto :quit

:choice
set /P c=Continue the build process? [Y/N]
if /I "%c%" EQU "Y" goto :continue
if /I "%c%" EQU "N" goto :quit
goto :choice

:continue
if exist custom_charts rmdir /Q /S custom_charts
Xcopy /E /I /Q /Y .\src\defaults .

ssc2museca\ssc2museca.exe --build-all
if %errorlevel% NEQ 0 (set /a error=1)

:quit
if %error% EQU 0 (
  echo   No errors^^! Everything is shiny :^)
  echo.
) else (
  echo.
  echo Error Summary:
  type error_log.txt
  echo.
)
cmd /k
