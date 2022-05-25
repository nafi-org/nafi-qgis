#!/bin/bash

mkdir deployment

# get a clean copy of the current branch in a subdirectory `deployment`
git archive HEAD | tar -x -C deployment
cd deployment

# remove bare image files—these are encoded in resources_rc anyway
cp naficp/images/icon.png naficp/icon.png
rm -rf naficp/images

# zip up the NAFI plug-in directory only into a datestamped archive
# zip -FSr "../ntrrp-$(date +'%Y%m%d').zip" ntrrp
# cd ..
# rm -rf deployment


