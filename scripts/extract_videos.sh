#!/bin/bash
# Execute scraper plugins for loading new videos.
# 
dir=$(dirname $(which $0));
cd $dir
cd ..
source ../ve/bin/activate

echo 'Extract videos...'

python manage.py find_youtube

