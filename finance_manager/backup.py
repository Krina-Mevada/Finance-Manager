import shutil
import os
from datetime import datetime

DB_PATH = "finance_manager.db"
BACKUP_FOLDER = "backup"
BACKUP_FILE = os.path.join(BACKUP_FOLDER,"finance_manager_backup.db")

def auto_backup():

    """Backs up the current database to the backup folder
       with a timestamp."""
    
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_FOLDER,backup_name)
    shutil.copyfile(DB_PATH, backup_path)
    print(f"Backup saved as {backup_name}")

def auto_restore():
    """Restores the most recent backup
       if the main db doesn't exist."""
    if os.path.exists(DB_PATH):
        return
    
    if not os.path.exists(BACKUP_FOLDER):
        print("!! No backup folder found.")
        return
    
    backups = [f for f in os.listdir(BACKUP_FOLDER) if f.endswith('.db')]
    if not backups:
        print("!! No backup files found.")
        return
    
    latest_backup = max(backups)
    latest_path = os.path.join(BACKUP_FOLDER,latest_backup)
    shutil.copyfile(latest_path,DB_PATH)
    print(f"Restored DB from {latest_backup}")