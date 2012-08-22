import time, os, subprocess
MINUTES = 15;
SENDMINUTES = 15;


if os.path.exists('/tmp/time'):	
	f=open('/tmp/time', 'r')
	readtime = f.readline().strip()
	difference = time.mktime(time.localtime()) - float(readtime)
	print difference
	f.close()
else:
	difference = MINUTES * 60 + 1


if difference > MINUTES * 60:
	
	tempfile = os.popen("pgrep -f tcpdump")
	pidlist = tempfile.readlines()
	tempfile.close()
	tempfile = os.popen("pgrep -f loop.py")
	pidlist = pidlist + tempfile.readlines()
	tempfile.close()
	for x in pidlist:
		os.popen("kill "+x)
	time.sleep(10)
	for x in pidlist:
		os.popen("kill -9 "+ x)
	os.popen("python loop.py")

if os.path.exists('/tmp/sendtime'):	
	f=open('/tmp/sendtime', 'r')
	readtime = f.readline().strip()
	difference = time.mktime(time.localtime()) - float(readtime)
	f.close
else:
	difference = SENDMINUTES * 60 + 1

if difference > SENDMINUTES * 60:
	tempfile = os.popen("pgrep -f sendmail.py")
	pidlist = tempfile.readlines()
	tempfile.close()
	for x in pidlist:
		os.popen("kill "+x)
	time.sleep(10)
	for x in pidlist:
		os.popen("kill -9 "+ x)
	os.popen("python sendmail.py")

#	subprocess.Popen("killall -q tcpdump".split(" "), shell=False)
#	subprocess.Popen("killall -q foo".split(" "), shell=False)
	
#	time.sleep(10)
	
#	subprocess.Popen("killall -9 -q tcpdump".split(" "), shell=False)
#	subprocess.Popen("killall -9 -q foo".split(" "), shell=False)
	
#	subprocess.Popen()
tempfile = os.popen("pgrep -f sendmail.py")
pidlist = tempfile.readlines()
tempfile.close()
if len(pidlist)>1:
	for x in pidlist:
		os.popen("kill "+x)
	time.sleep(10)
	for x in pidlist:
		os.popen("kill -9 "+ x)
	