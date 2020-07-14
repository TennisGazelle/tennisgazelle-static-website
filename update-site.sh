#!/bin/bash

#python3 image_fetcher.py

open docs/index.html

read CONTINUE "Continue?"

exit 0

git add docs/
git commit -m'[content update]'
git push