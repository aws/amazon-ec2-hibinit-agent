#!/bin/sh

PATH=/sbin:/bin:/usr/bin
failed='false'
hibernate()
{
        swapon /swap && /usr/sbin/pm-hibernate
        if [ $? -ne 0 ]
        then
            logger "Hibernation failed, Sleeping 2 mins before retry"
            failed='true'
        else
            failed='false'
        fi
        swapoff /swap
}

case "$2" in
    SBTN)
        # The iteration had been placed here to add retry logic to hibernation 
        # in case of failures and to avoid force stop of instances after 20min
        for i in 1 2 3
        do
          hibernate
          if [ $failed == 'true' ];
          then
            sleep 2m
          else
           break
          fi
       done
       ;;
    *)
        logger "ACPI action undefined: $2" ;;
esac
