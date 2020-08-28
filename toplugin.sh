#!/bin/bash

# "default" profile directory
PLUGIN_PATH=/mnt/c/Users/tflyn/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins

rm -rf $PLUGIN_PATH/nafi
cp -r nafi $PLUGIN_PATH

# global plug-in directory
# cp -r nafi /mnt/c/Program\ Files/QGIS\ 3.4/apps/qgis-ltr/python/plugins

