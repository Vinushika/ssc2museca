@echo off
setlocal ENABLEDELAYEDEXPANSION

set source=".\src\custom_charts"

if exist error_log.txt del error_log.txt

set error=0

::Verify assets
for /r %source% %%I in (*.ssc) do (
  ssc2museca\ssc2museca.exe "%%I" --verify
  echo -
  if !errorlevel! EQU 1 (set /a error=1)
 )
if %error% EQU 0 (echo   Verification success) else (echo   Verification failed.) && goto :quit

:choice
set /P c=Continue the build process? [Y/N]
if /I "%c%" EQU "Y" goto :continue
if /I "%c%" EQU "N" goto :quit
goto :choice

:continue
if exist custom_charts rmdir /Q /S museca-plus-modpack
Xcopy /E /I /Q /Y .\src\defaults .

for /r %source% %%I in (*.ssc) do (
  echo %%I
  ssc2museca\ssc2museca.exe "%%I"
)

:quit
cmd /k
