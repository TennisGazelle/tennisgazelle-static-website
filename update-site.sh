#!/bin/bash

#python3 image_fetcher.py

open docs/index.html

read CONTINUE "Continue?"

exit 0

cp docs/home.html docs/index.html

git add inputs/
git add docs/
git add carbon-config.json
git commit -m'[content update]'
git push