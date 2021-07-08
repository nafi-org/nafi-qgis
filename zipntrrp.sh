#!/bin/bash

mkdir deployment

# get a clean copy of the current branch in a subdirectory `deployment`
git archive HEAD | tar -x -C deployment
cd deployment

# remove bare image files—these are encoded in resources_rc anyway
cp ntrrp/images/icon.png nafi/icon.png
rm -rf ntrrp/images

# zip up the NAFI plug-in directory only into a datestamped archive
zip -FSr "../ntrrp-$(date +'%Y%m%d').zip" ntrrp
cd ..
rm -rf deployment


