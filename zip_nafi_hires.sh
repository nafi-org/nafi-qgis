#!/bin/bash

mkdir deployment

# get a clean copy of the current branch in a subdirectory `deployment`
git archive --verbose HEAD | tar -x -C deployment
cd deployment

# remove bare image files—these are encoded in resources.py anyway
cp nafi_hires/images/icon.png nafi_hires/icon.png
rm -rf nafi_hires/images

# remove unused scripts and bits and pieces
rm -rf nafi_hires/uic.bat
rm -rf nafi_hires/dev.py

find . -name "*.qss" | xargs rm -f

# zip up the NAFI HiRes plug-in directory only into a datestamped archive
zip a -r "../nafi_hires-$(date +'%Y%m%d').zip" nafi_hires
cd ..
rm -rf deployment
