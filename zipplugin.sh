#!/bin/bash

rm -f nafi-1.0.zip
mkdir deployment
git archive master | tar -x -C deployment
cd deployment
zip -FSr ../nafi-1.0.zip nafi
cd ..
rm -rf deployment


