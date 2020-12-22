#!/bin/sh

DATE=$(date +'%Y%m%d%H%M')
WEEK=$(date +'%Y%U')

sqlite=/usr/bin/sqlite3

# Garradin

db_path=/var/www/garradin/association.sqlite
backup_path=/data/backup/garradin

$sqlite $db_path ".backup $backup_path/association_daily_$DATE.sqlite"
$sqlite $db_path ".backup $backup_path/association_weekly_$WEEK.sqlite"

find $backup_path/association_daily* -mtime +182 -delete
find $backup_path/association_weekly* -mtime +500 -delete
