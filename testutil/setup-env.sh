#!/bin/bash
cd $HOME

VIRTUAL_ENV=NetShare
USERNAME=xinyu
CONDA_EXEC=$HOME/anaconda3/bin/conda
NETSHARE_LOCAL_REPO=/nfs/NetShare

# Anaconda3
if [ -f $CONDA_EXEC ] 
then
    echo "Anaconda3 installed."
else
    echo "Anaconda3 not installed. Start installation now..."
    wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
    bash Anaconda3-2022.05-Linux-x86_64.sh -b -p $HOME/anaconda3
fi
eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
conda init

if [ -f $CONDA_EXEC ] 
then
    echo "Anaconda3 installed."
else
    echo "Anaconda3 not installed. Start installation now..."
    wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
    bash Anaconda3-2022.05-Linux-x86_64.sh -b -p $HOME/anaconda3
fi
eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
conda init

# If already cloned
if ! [ -d $NETSHARE_LOCAL_REPO]
then
    echo "git clone from xinyu's fork of remote repo..."
#     git clone https://github.com/netsharecmu/NetShare.git $NETSHARE_LOCAL_REPO
    git clone https://github.com/Xinyu-Li-123/NetShare.git $NETSHARE_LOCAL_REPO
else
    echo "$NETSHARE_LOCAL_REPO exists! Skip git clone..."
fi