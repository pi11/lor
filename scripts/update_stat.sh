#!/bin/bash
# Execute scraper plugins for loading new videos.
# 
dir=$(dirname $(which $0));
cd $dir
cd ..
source ../ve/bin/activate
echo 'Updating forum messages...'
python manage.py update_forum_messages

echo 'Updating trololo...'
python manage.py update_trololo

echo 'Updating user stats...'
python manage.py update_user_stat


