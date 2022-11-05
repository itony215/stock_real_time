#!/bin/bash
cd /home/pineapple/Documents/stock/crawler/flat_viewer/stream_data/flat_viewer_data/
GIT_USERNAME=itony215
GIT_PASSWORD=
git add .  
git commit -m $(date +%y%m%d)
git push https://$GIT_USERNAME:$GIT_PASSWORD@github.com/itony215/flat_viewer_data.git --all