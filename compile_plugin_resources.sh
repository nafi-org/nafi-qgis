#!/bin/bash

# eg 'ntrrp', 'naficp', 'nafi' - needs to be a subdirectory of the current directory
plugin_name=$1
workingDir=$PWD

resourceFile="${workingDir}/${plugin_name}/resources.qrc"
targetFile="${workingDir}/${plugin_name}/resources_rc.py"

# compile in the resource format QGIS 3 reads
SOURCE_DATE_EPOCH=1 pyside6-rcc --format-version 2 --no-zstd "$resourceFile" -o "$targetFile"

# import Qt through qgis.PyQt
sed -i.bak 's/^from PySide6 import QtCore$/from qgis.PyQt import QtCore/' "$targetFile"
rm -f "$targetFile.bak"
