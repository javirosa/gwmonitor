import time, os, subprocess
from sys import maxint as MAXINT

MINUTES = 15;
SENDMINUTES = 15;
LOOPTIMER = '/tmp/time'
SENDMAILTIMER = '/tmp/sendtime'

"""Using pgrep searches for processes which have "key" as a substring."""
def getPIDList(key):
	tempfile = os.popen("pgrep -f " + key)
	pidlist = tempfile.readlines()
	tempfile.close()
	return pidlist

"""First asks process to stop and waits. Forcefully kills the process after the waittime."""
def killProcesses(pidlist,waitTime=10):
	for x in pidlist:
		os.popen("kill "+x)
	time.sleep(waitTime)
	for x in pidlist:
		os.popen("kill -9 "+ x)

"""Get's the amount of time since the timer was set. Returns the given unsetdefault value if the timer was not set."""
def timeElapsed(timer,unsetdefault=MAXINT):
	if os.path.exists(timer):	
		f=open(timer, 'r')
		readtime = f.readline().strip()
		f.close()
		difference = time.mktime(time.localtime()) - float(readtime)
		print difference
		return difference
	else:
		return unsetdefault

def main():
	print "checking loop.py"
	#If loop.py hasn't updated its timer in awhile kill and restart it
	difference = timeElapsed(LOOPTIMER,MINUTES*60+1)
	if difference > MINUTES * 60:
		pidlist = getPIDList("tcpdump") + getPIDList("loop.py")
		killProcesses(pidlist)
		os.popen("python loop.py")

	print "checking sendmail.py"
	#If sendmail.py hasn't updated its timer in awhile kill and restart it
	difference = timeElapsed(SENDMAILTIMER,SENDMINUTES*60+1)
	if difference > SENDMINUTES * 60:
		pidlist = getPIDList("sendmail.py")
		killProcesses(pidlist)
		os.popen("python sendmail.py")

	#TODO Why is this here? 
	pidlist = getPIDList("sendmail.py")
	if len(pidlist)>1:
		killProcesses(pidlist)

if __name__ == "__main__":
	main()
	
