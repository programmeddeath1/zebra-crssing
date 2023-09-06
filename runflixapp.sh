#!/bin/bash
SERVICE="next"
SERVICE1="gunicorn"
APP="futureapp"
while true;
do
	#if ps -ef | grep $APP | grep $SERVICE | grep -v grep >/dev/null
	if ps -ef | grep $SERVICE | grep $APP | grep -v grep >/dev/null && ps -ef | grep $SERVICE1 | grep $APP | grep -v grep >/dev/null;
	then
		echo "Service is running"
	else
		ps -ef | grep futureapp | grep -v grep | awk '{print $2}' | xargs kill -9 >/dev/null 2>&1
		source ~/venv/bin/activate
		cd ~/futureapp
		reflex run --env prod --loglevel debug & >> pineapplogs.txt
		sleep 600;
	fi
	sleep 5
done
