#!/bin/bash

rm -f nafi-1.0.zip
mkdir deployment

# get a clean copy of the current branch in a subdirectory `deployment`
git archive HEAD | tar -x -C deployment
cd deployment

# remove bare image files—these are encoded in resources_rc anyway
cp nafi/images/icon.png nafi/icon.png
rm -rf nafi/images

# zip up the NAFI plug-in directory only into a datestamped archive
zip -FSr "../nafi-$(date +'%Y%m%d').zip" nafi
cd ..
rm -rf deployment


