#!/bin/bash
# Execute scraper plugins for loading new videos.

#!/bin/bash
 
dir=$(dirname $(which $0));
cd $dir
cd ..
source ../ve/bin/activate

mypidfile=update-archive.pid
PID=$(<"$mypidfile")

if kill -0 $PID > /dev/null 2>&1;
then
   echo "Script is already runing, pid:[$PID]" >&2
   exit 1
fi

echo $$ > "$mypidfile"

python manage.py scan --forum 'Новости' --archive=1
python manage.py scan --forum='linux-org-ru' --archive=1
python manage.py scan --forum=security --archive=1
python manage.py scan --forum='linux-hardware' --archive=1
python manage.py scan --forum=job --archive=1
python manage.py scan --forum=games --archive=1
python manage.py scan --forum='web-development' --archive=1
python manage.py scan --forum='lor-source' --archive=1
python manage.py scan --forum=mobile --archive=1
python manage.py scan --forum=multimedia --archive=1
python manage.py scan --forum=midnight --archive=1
python manage.py scan --forum=gallery --archive=1
python manage.py scan --forum=science --archive=1
python manage.py scan --forum=клуб --archive=1
python manage.py scan --forum=talks --archive=1
python manage.py scan --forum=general --archive=1
python manage.py scan --forum=desktop --archive=1
python manage.py scan --forum=admin --archive=1
python manage.py scan --forum='linux-install' --archive=1
python manage.py scan --forum=development --archive=1



# Ensure PID file is removed on program exit.
trap "rm -f -- '$mypidfile'" EXIT





