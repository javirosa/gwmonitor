#!/bin/sh
#first argument is IP and second is password for the root acount on the routerstation
#Uses ssh to execute installation commands on the remote RS

IP=$1
INSTALL_DIR="/root/"
FILES="loop.py runcheck.py sendmail.py"
CHECKER="runcheck.py"
TMP="root.crontab.bak"
CRONJOB='    *        *          *             *               *           python /root/runcheck.py'
CRONPATH="/etc/crontabs/root"

echo IP:$1

#Copy files
scp $FILES root@$IP:"$INSTALL_DIR"

#add entry to crontab TODO check if it is already there
scp root@$IP:"$CRONPATH" $TMP
if egrep $CHECKER $TMP >>/dev/null
then
    echo "Already installed please remove the line with $CHECKER in the $CRONPATH file and delete $FILES from $INSTALL_DIR directory."
else
    ssh root@"$IP" echo "$CRONJOB" >> "$CRONPATH"
fi
rm "$TMP"
