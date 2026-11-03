#!/bin/bash

FolderToBackup="$HOME/test-folder"
BackupDestination="$HOME/backups"
BackupTime=$(date +%F)
BackupName=$BackupDestination/backup-$BackupTime

mkdir -p "$BackupDestination"

cp -r "$FolderToBackup" "$BackupName"

