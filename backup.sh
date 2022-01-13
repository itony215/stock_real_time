#!/bin/bash

foldername=5K_$(date +%m%d)
cp -r -p /home/pitaya/Documents/stock/5K/ /home/pitaya/Documents/stock/backup/
mv /home/pitaya/Documents/stock/backup/5K /home/pitaya/Documents/stock/backup/${foldername}
rm -r /home/pitaya/Documents/stock/5K/*
