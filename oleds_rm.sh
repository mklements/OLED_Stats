#!/bin/bash
# OLED Stats Cleanup Script
# Removes all files, directories, virtualenv, and crontab entries created by autoinstall_oled_stats.sh

set -e
cd "$HOME" || exit 1

echo "OLED Stats Cleanup Script"
echo "------------------------"

USER_HOME="$HOME"
if [ "$USER" = "root" ]; then
    ACTUAL_USER=$(who am i | awk '{print $1}')
    if [ -n "$ACTUAL_USER" ]; then
        USER_HOME="/home/$ACTUAL_USER"
    fi
fi

echo "Detected home directory: $USER_HOME"
echo

# List of items to check and remove
ITEMS_TO_REMOVE=(
    "$USER_HOME/stats_env"
    "$USER_HOME/rpi_oled_stats"
    "$USER_HOME/oled_display_start.sh"
)

echo "The following items will be removed if they exist:"
for ITEM in "${ITEMS_TO_REMOVE[@]}"; do
    if [ -e "$ITEM" ]; then
        echo "  $ITEM"
    else
        echo "  $ITEM (not found)"
    fi
done

# Check for crontab entry
CRON_PATTERN="oled_display_start.sh"
CRON_EXISTS=false
if crontab -l 2>/dev/null | grep -q "$CRON_PATTERN"; then
    CRON_EXISTS=true
    echo "  Crontab entry containing: $CRON_PATTERN"
else
    echo "  Crontab entry containing: $CRON_PATTERN (not found)"
fi

echo
read -p "Proceed with removal? [y/N]: " CONFIRM < /dev/tty
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Remove files/directories
for ITEM in "${ITEMS_TO_REMOVE[@]}"; do
    if [ -e "$ITEM" ]; then
        rm -rf "$ITEM"
        echo "Removed: $ITEM"
    fi
done

# Remove crontab entry
if [ "$CRON_EXISTS" = true ]; then
    crontab -l 2>/dev/null | grep -v "$CRON_PATTERN" | crontab -
    echo "Removed crontab entry containing: $CRON_PATTERN"
fi

echo "Cleanup complete."
