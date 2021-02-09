#!/bin/bash

python3 image_fetcher.py

git add docs/
git commit -m'[content update]'
git push