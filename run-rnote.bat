@echo off
set "PATH=C:\msys64\clangarm64\bin;%PATH%"
set "GSETTINGS_SCHEMA_DIR=C:\msys64\clangarm64\share\glib-2.0\schemas"
start "" "%~dp0_mesonbuild\rnote.exe"
