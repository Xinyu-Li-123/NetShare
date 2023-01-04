#!/bin/bash
KEY_FILE=~/.ssh/id_rsa
if [ -f "$KEY_FILE" -a -f "$KEY_FILE.pub" ]; then
    echo "An existing ssh key pair has been found." >> /nfs/testfile
else
    echo "Generating ssh key pair..."  >> /nfs/testfile
    ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa <<< y
fi
cat ~/.ssh/id_rsa.pub >> /nfs/id_agg.pub
exit
