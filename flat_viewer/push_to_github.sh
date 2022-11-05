#!/bin/bash
cd /home/pineapple/Documents/stock/crawler/flat_viewer/stream_data/flat_viewer_data/
GIT_USERNAME=itony215
GIT_PASSWORD=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
git add .  
git commit -m $(date +%y%m%d)
git push https://$GIT_USERNAME:$GIT_PASSWORD@github.com/itony215/flat_viewer_data.git --all