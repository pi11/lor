#!/bin/bash

dir=$(dirname $(which $0));
cd $dir
cd ..
source ../ve/bin/activate

mypidfile=updatetalks.pid
PID=$(<"$mypidfile")

if kill -0 $PID > /dev/null 2>&1;
then
   echo "Script is already runing, pid:[$PID]" >&2
   exit 1
fi

echo $$ > "$mypidfile"

python manage.py scan --forum talks


# Ensure PID file is removed on program exit.
trap "rm -f -- '$mypidfile'" EXIT
