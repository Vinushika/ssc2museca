@echo off
setlocal ENABLEDELAYEDEXPANSION

if "%~1" NEQ "" (
  for /F "delims=" %%B in ('dir /S /B "%~1\*.ssc"') do set source=%%B
  goto :next
) else (
  goto :input
)

:input
echo Enter the name of the ssc file. (e.g. 1116.ssc)
set /P file=
for /F "delims=" %%B in ('dir /S /B "src\!file!"') do set source=%%B && goto :next
goto :quit

:next
ssc2museca\ssc2museca.exe -f "%source%"

:quit
cmd /k
