#!/bin/bash

# eg 'ntrrp', 'naficp', 'nafi' - needs to be a subdirectory of the current directory
plugin_name=$1

workingDir=$PWD

version=$(grep '^version=' "plugins/${plugin_name}/metadata.txt" | cut -d= -f2)
archiveName="${workingDir}/${plugin_name}-${version}.zip"

if [ -f "${archiveName}" ]; then
    read -rp "${archiveName} already exists. Overwrite? [y/N] " answer
    if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
        echo "Aborted."
        exit 1
    fi
    rm "${archiveName}"
fi

echo "Creating a release package for ${plugin_name} v${version}"

mkdir deployment

# get a clean copy of the current branch in a subdirectory `deployment`
git archive HEAD | tar -x -C deployment
cd deployment/plugins || exit

# remove any bare image files—these are encoded in resources_rc anyway
cp "${plugin_name}/images/icon.png" "${plugin_name}/icon.png"
# rm -rf "${plugin_name}/images"

# include the repository LICENSE alongside the plugin
cp "../LICENSE" "${plugin_name}/LICENSE"

# zip up the ${plugin_name} directory only into a versioned archive
zip -rq "${archiveName}" "${plugin_name}"

cd "${workingDir}" || exit
rm -rf deployment

echo "Created ${archiveName}"
