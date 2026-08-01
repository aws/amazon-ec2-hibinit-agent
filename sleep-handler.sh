#!/bin/bash

# This is called before hibernating or after resuming, as follows:
# $0=/usr/lib/systemd/system-sleep/sleepyhead, $1=pre, $2=suspend
# ...and when the lid is opened, as follows:
# $0=/usr/lib/systemd/system-sleep/sleepyhead, $1=post, $2=suspend

HIBERNATE_STATE_DIR=/var/run/hibernate
RESUMED_AT="$HIBERNATE_STATE_DIR/resumed_at"
LOGNAME="hibernate"

log() {
    logger -t "$LOGNAME" "[PID $$] $1"
}

if [ "$1" = "post" ]; then
    resumed_time=$(date +%s)
    log "Resumed at $resumed_time"
    echo "$resumed_time" > "$RESUMED_AT"

    if swapon --show | grep -q '/swap'; then
        log "Disabling /swap post resume"
        if swapoff /swap; then
            log "/swap disabled successfully"
        else
            log "ERROR: Failed to disable /swap"
        fi
    else
        log "/swap not active, skipping swapoff"
    fi
fi
