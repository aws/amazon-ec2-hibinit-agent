#!/bin/bash
  
# This is called before hibernating or after resuming, as follows:
# $0=/usr/lib/systemd/system-sleep/sleepyhead, $1=pre, $2=suspend
# ...and when the lid is opened, as follows:
# $0=/usr/lib/systemd/system-sleep/sleepyhead, $1=post, $2=suspend

if [ "$1" = "post" ] ; then
    logger "Resuming from sleep to swapoff"
    swapoff /swap
fi
