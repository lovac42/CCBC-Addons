@echo off
set ZIP=C:\PROGRA~1\7-Zip\7z.exe a -tzip -y -r
set REPO=kanji_stats
set NAME=kanji_stats
set PACKID=kanji_stats
set VERSION=0.0.1


echo %VERSION% >%REPO%\VERSION

fsum -r -jm -md5 -d%REPO% * > checksum.md5
move checksum.md5 %REPO%\checksum.md5

REM %ZIP% %REPO%_v%VERSION%_Anki20.zip *.py %REPO%\*

cd %REPO%

REM quick_manifest.exe "%NAME%" "%PACKID%" >manifest.json
REM %ZIP% ../%REPO%_v%VERSION%_Anki21.ankiaddon *

quick_manifest.exe "%NAME%" "%NAME%" >manifest.json
%ZIP% ../%REPO%_v%VERSION%_CCBC.adze *
