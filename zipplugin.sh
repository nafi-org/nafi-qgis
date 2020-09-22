#!/bin/bash

rm -f nafi-1.0.zip
mkdir deployment
git archive feature/NAFI-Release-Candidate | tar -x -C deployment
cd deployment

# remove bare image files—these are encoded in resources_rc anyway
cp nafi/images/icon.png nafi/icon.png
rm -rf nafi/images
zip -FSr ../nafi-1.0.zip nafi
cd ..
rm -rf deployment


