#!/bin/bash

# Runs on resume from hibernation via the systemd system-sleep hook:
#   $1=post $2=hibernate
#
# Records the resume time so acpid.sleep.sh's should_hibernate() can debounce a
# spurious sleep-button event that arrives shortly after a resume.
#
# We intentionally do NOT swapoff /swap here. After a successful resume the
# kernel has already invalidated the hibernation image (the swap signature is
# reset during resume), so the swap area is just ordinary swap again and does
# not need tearing down. swapoff would have to page the entire image back into
# RAM synchronously; on a memory-heavy host that cannot fit, swapoff blocks in
# uninterruptible (D) state and freezes the instance.

HIBERNATE_STATE_DIR=/var/run/hibernate
RESUMED_AT="$HIBERNATE_STATE_DIR/resumed_at"
LOGNAME="hibernate"

log() {
    logger -t "$LOGNAME" "[PID $$] $1"
}

if [ "$1" = "post" ]; then
    resumed_time=$(date +%s)
    log "Resumed at $resumed_time"
    mkdir -p "$HIBERNATE_STATE_DIR"
    echo "$resumed_time" > "$RESUMED_AT"
fi
