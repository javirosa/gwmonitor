#!/bin/python
import os, subprocess, time, shutil
import deamonize

SRC = "/root/"
DST = "/tmp/send/"
senddir = "/tmp/send/"
capdir = "/tmp/cap/"
CAPSIZE = 70

def initializecapture():
	
	if not os.path.exists(senddir):
		os.makedirs(senddir)
		
	if not os.path.exists(capdir):
		os.makedirs(capdir)
	tcpdump = subprocess.Popen(["tcpdump", "-s", str(CAPSIZE), "-w", "/tmp/cap/capture.pcap"], shell=False)
	pid = str(tcpdump.pid)
	f = open('/tmp/pid', 'w')
	f.write(pid)
	f.close();
	time.sleep(1)

	f=open('/tmp/time', 'w')
	f.write("%100.100s"%(str(time.mktime(time.localtime()))))
	f.close()


	
def capture():	
	
	if os.path.exists('/tmp/time'):	
		f=open('/tmp/time', 'r')
		readtime = f.readline().strip()
		difference = time.mktime(time.localtime()) - float(readtime)
		f.close()
	else:
		difference = 0
	
	
	if (os.path.getsize('/tmp/cap/capture.pcap')>3000000) or (difference > 86400):
		f = open('/tmp/pid', 'r')
		#kill old tcpdump process
		pid = f.read()
		f.close()
		subprocess.Popen("kill " + pid, shell=True)
		print "killing old"
		
		localtime = time.strftime( "%Y-%m-%d___%H-%M-%S")
		print "Local current time :", localtime
	#	localtime = localtime + ".tar.gz"
	#	shutil.move('cap/capture.pcap', 'cap/'+localtime+'.pcap')

	#	temp = subprocess.Popen("gzip -1 cap/capture.pcap" , shell=True)
		
	#	temp.wait();
		shutil.move('/tmp/cap/capture.pcap', '/tmp/send/' +localtime+'.pcap')
		tcpdump = subprocess.Popen(["tcpdump", "-s", str(CAPSIZE), "-w", "/tmp/cap/capture.pcap"], shell=False)
	#	shutil.move("cap/" +localtime+".pcap.gz", "send/" + localtime+".pcap.gz")
	#	os.remove('cap/capture2compress.pcap')
		
		#subprocess.Popen("mv" + " " + "cap/*.gz" + " " + DST,shell=True)
		
		pid = str(tcpdump.pid)
		f = open('/tmp/pid', 'w')
		f.write(pid)
		f.close();
		f=open('/tmp/time', 'w')
		f.write("%100.100s"%(str(time.mktime(time.localtime()))))
		f.close()
		time.sleep(5)
		
if __name__ == "__main__":

	#retCode = deamonize.createDaemon()

	initializecapture()
	while 1:
		capture()
	sys.exit(retCode)

