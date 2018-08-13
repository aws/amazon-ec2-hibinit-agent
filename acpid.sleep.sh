#!/bin/sh

PATH=/sbin:/bin:/usr/bin
case "$2" in
    SBTN)
        swapon /swap && /usr/sbin/pm-hibernate
        swapoff /swap
        ;;
    *)
        logger "ACPI action undefined: $2" ;;
esac
