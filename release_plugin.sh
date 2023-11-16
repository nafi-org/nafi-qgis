#!/bin/bash

# eg 'ntrrp', 'naficp', 'nafi' - needs to be a subdirectory of the current directory
plugin_name=$1

workingDir=$PWD

unameOutput="$(uname -s)"
case "${unameOutput}" in
    Linux*)     osName=Linux;;
    Darwin*)    osName=Mac;;
    CYGWIN*)    osName=Cygwin;;
    MINGW*)     osName=MinGw;;
    MSYS_NT*)   osName=Git;;
    *)          osName="UNKNOWN:${unameOutput}"
esac

archiveName="${workingDir}/${plugin_name}-$(date +'%Y%m%d').zip"

echo Creating a release package for ${plugin_name}
echo Detected OS ${osName}, using zip command ${zipCmd} to create ${archiveName}

mkdir deployment

# get a clean copy of the current branch in a subdirectory `deployment`
git archive HEAD | tar -x -C deployment
cd deployment

# remove any bare image files—these are encoded in resources_rc anyway
cp ${plugin_name}/images/icon.png ${plugin_name}/icon.png
# rm -rf ${plugin_name}/images


# zip up the ${plugin_name} directory only into a datestamped archive
if [ ${osName} == "Mac" ]; then
    zip -rq "../${plugin_name}-$(date +'%Y%m%d').zip" ${plugin_name}
else
    7z a -r "../${plugin_name}-$(date +'%Y%m%d').zip" ${plugin_name}
fi

cd ..
rm -rf deployment

echo Created ${archiveName}
