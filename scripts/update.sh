#!/bin/bash
# Execute scraper plugins for loading new videos.

#!/bin/bash
 
dir=$(dirname $(which $0));
cd $dir
cd ..
source ../ve/bin/activate

mypidfile=update.pid
PID=$(<"$mypidfile")

if kill -0 $PID > /dev/null 2>&1;
then
   echo "Script is already runing, pid:[$PID]" >&2
   exit 1
fi

echo $$ > "$mypidfile"

python manage.py scan --forum 'Новости'
python manage.py scan --forum='linux-org-ru'
python manage.py scan --forum=security
python manage.py scan --forum='linux-hardware'
python manage.py scan --forum=job
python manage.py scan --forum=games
python manage.py scan --forum='web-development'
python manage.py scan --forum='lor-source'
python manage.py scan --forum=mobile
python manage.py scan --forum=multimedia
python manage.py scan --forum=midnight
python manage.py scan --forum=gallery
python manage.py scan --forum=science
python manage.py scan --forum=клуб
python manage.py scan --forum=talks
python manage.py scan --forum=general
python manage.py scan --forum=desktop
python manage.py scan --forum=admin
python manage.py scan --forum='linux-install'
python manage.py scan --forum=development



# Ensure PID file is removed on program exit.
trap "rm -f -- '$mypidfile'" EXIT





