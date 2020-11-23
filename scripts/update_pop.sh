#!/bin/bash
# Execute scraper plugins for loading new videos.
# 
dir=$(dirname $(which $0));
cd $dir
cd ..
source ../ve/bin/activate
python manage.py scan talks
