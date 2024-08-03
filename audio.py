import os
import shutil
import time
import threading
import psutil

source_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'Roblox', 'sounds')
destination_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'sound_backup')

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

processed_files = set()

def copy_and_rename_file(src_path):
    try:
        original_filename = os.path.basename(src_path)
        new_filename = f"{os.path.splitext(original_filename)[0]}.ogg"
        backup_path = os.path.join(destination_dir, new_filename)
        
        shutil.copy2(src_path, backup_path)
        print(f'File copied and renamed to: {new_filename}')
    except Exception as e:
        print(f'Error copying file {os.path.basename(src_path)}: {e}')

def process_file(file_path):
    filename = os.path.basename(file_path)
    if filename not in processed_files:
        copy_and_rename_file(file_path)
        processed_files.add(filename)

def check_for_new_files():
    while True:
        try:
            current_files = set(os.listdir(source_dir))
            new_files = current_files - processed_files

            for filename in new_files:
                file_path = os.path.join(source_dir, filename)
                if os.path.isfile(file_path):
                    process_file(file_path)

            time.sleep(1)
        except Exception as e:
            print(f'Error checking for new files: {e}')
            time.sleep(1)

def is_roblox_client_running():
    for proc in psutil.process_iter(['name']):
        if 'RobloxPlayerBeta' in proc.info['name']:
            return True
    return False

def clean_up_sounds_directory():
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print('Cleaned up old files in the sounds directory.')

if __name__ == "__main__":
    print('Welcome! This script helps you grab audio files from Roblox games.')
    print('It monitors the Roblox client’s folder for new audio files and copies them to a backup directory.')
    print('Note: While the audio files may work, some audio players might have difficulty playing them.')
    print('Note: The .ogg files do not retain their original asset names because Roblox encrypts the original file names.')
    print('This encryption makes it difficult to determine the original uploaded file name.')

    print('Cleaning up old files in the sounds directory...')
    clean_up_sounds_directory()

    print('Waiting for the Roblox client to start...')
    while not is_roblox_client_running():
        time.sleep(1)

    print('Roblox client detected. Starting file monitoring...')

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            process_file(file_path)

    monitoring_thread = threading.Thread(target=check_for_new_files)
    monitoring_thread.daemon = True
    monitoring_thread.start()

    try:
        while is_roblox_client_running():
            time.sleep(1)
    except KeyboardInterrupt:
        print('Stopped by user')

    clean_up_sounds_directory()
    print('Roblox client has closed. Exiting...')
