ps -ef | grep futureapp | grep -v grep | awk '{print $2}' | xargs kill -9
#ps -ef | grep reflex | grep -v grep | awk '{print $2}' | xargs kill -9
ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -9

