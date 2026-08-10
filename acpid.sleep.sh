#!/bin/sh

PATH=/sbin:/bin:/usr/bin

# Hibernation selects the swapfile with highest priority. Since there may be
# other swapfiles configured, ensure /swap is selected as hibernation
# target by setting to maximum priority.
swap_priority=32767

LOCKFILE=/var/run/hibernate.lock
HIBERNATE_STATE_DIR=/var/run/hibernate
HIBERNATED_AT="$HIBERNATE_STATE_DIR/hibernated_at"
RESUMED_AT="$HIBERNATE_STATE_DIR/resumed_at"
STALE_THRESHOLD=30
LOGNAME="hibernate"

log() {
    local level="$1"
    local message="$2"
    logger -t "$LOGNAME" -p "user.$level" "[PID $$] $message"
}

should_hibernate() {
    local now=$(date +%s)

    if [ -f "$RESUMED_AT" ]; then
        local resumed=$(cat "$RESUMED_AT" 2>/dev/null)
        if [ -n "$resumed" ] && [ "$resumed" -eq "$resumed" ] 2>/dev/null; then
            local since_resume=$((now - resumed))

            if [ $since_resume -lt $STALE_THRESHOLD ]; then
                log notice "Resumed ${since_resume}s ago, skipping"
                return 1
            fi
        fi

        return 0
    fi

    if [ -f "$HIBERNATED_AT" ]; then
        local hibernated=$(cat "$HIBERNATED_AT" 2>/dev/null)
        if [ -n "$hibernated" ] && [ "$hibernated" -eq "$hibernated" ] 2>/dev/null; then
            local since_hibernate=$((now - hibernated))

            if [ $since_hibernate -lt $STALE_THRESHOLD ]; then
                log notice "Hibernation started ${since_hibernate}s ago, skipping"
                return 1
            fi

            log notice "Stale hibernated_at (${since_hibernate}s old), clearing"
        fi

        rm -f "$HIBERNATED_AT"
        return 0
    fi

    return 0
}

do_hibernate() {
    local event="$1"

    for i in 1 2 3; do
        # Swap must be on to hibernate. Only enable it if /swap is not
        # already active so a pre-existing swap is left untouched.
        if swapon --show | grep -q '/swap'; then
            log notice "Attempt $i/3: /swap already active"
        else
            log notice "Attempt $i/3: Enabling swap"
            if ! swapon --priority=$swap_priority /swap; then
                log err "Attempt $i/3: Failed to enable swap, retrying in 10s"
                sleep 10
                continue
            fi
        fi

        log notice "Attempt $i/3: Swap enabled, initiating hibernation"
        sleep 1

        if systemctl hibernate; then
            log notice "Hibernation initiated"
            return 0
        else
            log err "Attempt $i/3: Hibernation initiation failed, disabling swap, retrying in 10s"
            swapoff /swap
            sleep 10
        fi
    done

    log err "All hibernation attempts failed"
    rm -f "$HIBERNATED_AT"
    return 1
}

mkdir -p "$HIBERNATE_STATE_DIR"

case "$2" in
    LNXSLPBN:*|SBTN)
        if ! should_hibernate; then
            log notice "ACPI event $2 ignored"
            exit 0
        fi

        rm -f "$RESUMED_AT"
        hibernated_time=$(date +%s)
        log notice "Hibernation requested at $hibernated_time"
        echo "$hibernated_time" > "$HIBERNATED_AT"

        exec 200>"$LOCKFILE"

        if flock -n 200; then
            log notice "ACPI event $2 received, initiating hibernation"
            do_hibernate "$2"
        else
            log notice "ACPI event $2 ignored, hibernation already in progress"
        fi
        ;;
    *)
        log warning "Unknown ACPI event: $2"
        ;;
esac
