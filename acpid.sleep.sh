#!/usr/bin/bash

PATH=/sbin:/bin:/usr/bin
failed='false'

# Hibernation selects the swapfile with highest priority. Since there may be
# other swapfiles configured, ensure /swap is selected as hibernation
# target by setting to maximum priority.
swap_priority=32767

set -x

case "$2" in
    SBTN|LNXSLPBN:*)
        # The iteration had been placed here to add retry logic to hibernation 
        # in case of failures and to avoid force stop of instances after 20min
        logger -t hibernate -p user.notice "Got $2 event, going to hibernate"
        for i in 1 2 3
        do
          if swapon --priority=$swap_priority /swap && sleep 1 && systemctl hibernate; then
                break
          else
                logger -t hibernate -p user.notice "Failed iteration $i"
                swapoff /swap
                sleep 10
          fi
       done
       ;;
    *)
        logger -t hibernate "ACPI action undefined: $2" ;;
esac
