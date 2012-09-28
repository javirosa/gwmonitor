import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os, subprocess, time
import daemonize

SMTP_USER = "monitoring@green-wifi.com"
SMTP_PWD = "green4chuuk"
EMAIL_TO = "javirosa1912@berkeley.edu"

SENDMAILTIMER = "/tmp/sendtime"
SENDDIR = "/tmp/send/"

#tempfile = os.popen("pgrep -f sendmail.py")
#pidlist = tempfile.readlines()
#tempfile.close()
#if len(pidlist) > 1:
#	print len(pidlist)
#	exit()
	
def mail(to, subject, text, attach):
	msg = MIMEMultipart()
	print "1"
	msg['From'] = SMTP_USER
	msg['To'] = to
	msg['Subject'] = subject
	print "2"
	msg.attach(MIMEText(text))
	print "3"
	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open(attach, 'rb').read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition',
	'attachment; filename="%s"' % os.path.basename(attach))
	msg.attach(part)
	print "4"
	mailServer = smtplib.SMTP("smtp.1and1.com", 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	print "5"
	mailServer.login(SMTP_USER, SMTP_PWD)
	print "6"	
	mailServer.sendmail(SMTP_USER, to, msg.as_string())
	print "7"
	mailServer.close()

def loop():
	while 1:
		rootdir = SENDDIR
		if os.path.exists(SENDMAILTIMER):
			f=open(SENDMAILTIMER, 'r+')
		else:
			f=open(SENDMAILTIMER, 'w')
			f.close
			f=open(SENDMAILTIMER, 'r+')
		f.write("%100.100s"%(str(time.mktime(time.localtime()))))
		f.seek(0,0)
	#	for subdir, dirs, files in os.walk(rootdir):
		if os.path.exists(rootdir):
			for mailFile in os.listdir(rootdir):
				filename = rootdir + mailFile
				print "Sending file %s"%(filename)
				#TODO handle failure to contact server, etc
				mail(EMAIL_TO,
					time.strftime( "%Y-%m-%d___%H-%M-%S"),
					"test",
					filename)
				print "file %s sent."%(filename)
				os.remove(filename)
				f=open(SENDMAILTIMER, 'w')
				f.write("%100.100s"%(str(time.mktime(time.localtime()))))
				f.seek(0,0)
        time.sleep(.01)
		
	f.close()		

if __name__ == "__main__":
	retCode = daemonize.createDaemon()
	loop()
	sys.exit(retCode)
	
