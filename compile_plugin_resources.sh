#!/bin/bash

# eg 'ntrrp', 'naficp', 'nafi' - needs to be a subdirectory of the current directory
plugin_name=$1
workingDir=$PWD

export PATH=/Applications/QGIS-LTR.app/Contents/MacOS/bin:$PATH
pythonCmd=$(which python3.9)

unameOutput="$(uname -s)"
case "${unameOutput}" in
    Linux*)     osName=Linux;;
    Darwin*)    osName=Mac;;
    CYGWIN*)    osName=Cygwin;;
    MINGW*)     osName=MinGw;;
    MSYS_NT*)   osName=Git;;
    *)          osName="UNKNOWN:${unameOutput}"
esac

resourceFile="${workingDir}/${plugin_name}/resources.qrc"
targetFile="${workingDir}/${plugin_name}/resources_rc.py"

exec $pythonCmd -m PyQt5.pyrcc_main $resourceFile -o $targetFile
