@echo off
setlocal ENABLEDELAYEDEXPANSION

::Usage- Set the source dir, optionally set the ID for batch conversion.
::ID specified in the .ssc file will always take precedence.
::Converter creates a custom_charts folder in the directory the script was run, and
:: automatically creates and updates a music-info-b.xml. If you wish to create an isolated
:: xml, uncomment the new_xml_dir variable and switch the comment in the for loop below.

set source="D:\Museca-Customs\to_convert"
::set new_xml_dir="D:\Museca-Customs"
set ID=227
if exist jacket_errors.txt del jacket_errors.txt

for /r %source% %%i in (*.ssc) do (
  echo %%i

  REM Uncomment this for isolated xml
  REM ssc2museca.py "%%i" -x !new_xml_dir! -id !ID!
    
  REM Use this for normal conversion.
  ssc2museca.py "%%i" -id !ID!
  set /a ID+=1
 )

cd D:\Museca-Customs\
cmd /k
