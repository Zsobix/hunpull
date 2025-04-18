#!/bin/sh
git pull
rm -rf hungary.m3u
python3 pull.py
git config --global user.name '<YOUR USERNAME>'
git config --global user.email '<YOUR USERNAME>@users.noreply.github.com'
git add hungary.m3u
git commit -m "m3u update"
git push
