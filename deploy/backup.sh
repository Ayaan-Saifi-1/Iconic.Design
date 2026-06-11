#!/bin/bash
# Free Backup Script for VPS
# This script will backup your SQLite databases and uploads directory.
# It uses local storage on the server but zips them and rotates them to save space.
# Set up a cronjob for this script:
# 0 2 * * * /path/to/your/app/deploy/backup.sh

# Directory of your application
APP_DIR="/path/to/your/app"
# Directory to store backups
BACKUP_DIR="$APP_DIR/backups"
# Date format for the backup filename
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "Starting backup: $BACKUP_FILE"

# Go to app directory
cd "$APP_DIR" || exit

# Create the archive (backup buildcorp.db, iconickitchen.db, and static/uploads if it exists)
tar -czf "$BACKUP_FILE" buildcorp.db iconickitchen.db static/uploads/ 2>/dev/null || tar -czf "$BACKUP_FILE" buildcorp.db iconickitchen.db

echo "Backup completed successfully."

# Keep only the last 7 backups to avoid filling up the server disk
echo "Cleaning up old backups (keeping last 7 days)..."
find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +7 -exec rm {} \;
echo "Cleanup done."
