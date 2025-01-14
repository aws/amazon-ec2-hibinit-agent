#!/bin/sh

PATH=/sbin:/bin:/usr/bin
failed='false'

# Hibernation selects the swapfile with highest priority. Since there may be
# other swapfiles configured, ensure /swap is selected as hibernation
# target by setting to maximum priority.
swap_priority=32767

hibernate()
{
        swapon --priority=$swap_priority /swap && systemctl hibernate
        if [ $? -ne 0 ]; then
            logger "Hibernation failed, Sleeping 2 mins before retry"
            failed='true'
            swapoff /swap
            sleep 2m
        else
            failed='false'
        fi
}

case "$2" in
    SBTN)
        # The iteration had been placed here to add retry logic to hibernation 
        # in case of failures and to avoid force stop of instances after 20min
        for i in 1 2 3; do
          hibernate
          if [ $failed == 'false' ]; then
            break
          fi
       done
       ;;
    *)
        logger "ACPI action undefined: $2" ;;
esac
