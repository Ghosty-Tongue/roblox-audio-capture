import os
import shutil
import time
import threading
import psutil
import logging
from queue import Queue

source_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'Roblox', 'sounds')
http_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'Roblox', 'http')
destination_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'sound_backup')

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

logging.basicConfig(filename='roblox_sound_backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

file_queue = Queue()
processed_files = set()
lock = threading.Lock()

def copy_and_rename_file(src_path):
    try:
        original_filename = os.path.basename(src_path)
        new_filename = f"{os.path.splitext(original_filename)[0]}.ogg"
        backup_path = os.path.join(destination_dir, new_filename)
        
        shutil.copy2(src_path, backup_path)
        print(f"File copied and renamed to: {new_filename}")
        logging.info(f'File copied and renamed to: {new_filename}')
    except Exception as e:
        print(f"Error copying file {os.path.basename(src_path)}: {e}")
        logging.error(f'Error copying file {os.path.basename(src_path)}: {e}')

def worker():
    while True:
        file_path = file_queue.get()
        if file_path is None:
            break
        print(f"Processing file: {file_path}")
        copy_and_rename_file(file_path)
        file_queue.task_done()

def process_file(file_path):
    filename = os.path.basename(file_path)
    with lock:
        if filename not in processed_files:
            print(f"Queueing new file for processing: {filename}")
            processed_files.add(filename)
            file_queue.put(file_path)

def check_for_new_files():
    while True:
        try:
            current_files = set(os.listdir(source_dir))
            new_files = current_files - processed_files

            for filename in new_files:
                file_path = os.path.join(source_dir, filename)
                if os.path.isfile(file_path):
                    print(f"Found new file: {filename}")
                    process_file(file_path)

            time.sleep(0.1)
        except Exception as e:
            print(f"Error checking for new files: {e}")
            logging.error(f'Error checking for new files: {e}')
            time.sleep(1)

def is_roblox_client_running():
    for proc in psutil.process_iter(['name']):
        if 'RobloxPlayerBeta' in proc.info['name']:
            return True
    return False

def clean_up_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print(f"Cleaned up files in the directory: {directory}")
    logging.info(f'Cleaned up files in the directory: {directory}')

if __name__ == "__main__":
    print('Welcome! This script helps you grab audio files from Roblox games.')
    print('It monitors the Roblox client’s folder for new audio files and copies them to a backup directory.')
    print('Note: The .ogg files do not retain their original asset names because Roblox encrypts the original file names.')
    print('This encryption makes it difficult to determine the original uploaded file name.')

    logging.info('Cleaning up old files in the sounds and http directories...')
    clean_up_directory(source_dir)
    clean_up_directory(http_dir)

    print('Waiting for the Roblox client to start...')
    while not is_roblox_client_running():
        time.sleep(1)

    logging.info('Roblox client detected. Starting file monitoring...')
    print('Roblox client detected. Starting file monitoring...')

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            print(f"Processing existing file: {filename}")
            process_file(file_path)

    num_worker_threads = 4
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)

    monitoring_thread = threading.Thread(target=check_for_new_files)
    monitoring_thread.daemon = True
    monitoring_thread.start()

    try:
        while is_roblox_client_running():
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info('Stopped by user')
        print('Stopped by user')

    for i in range(num_worker_threads):
        file_queue.put(None)
    for t in threads:
        t.join()

    clean_up_directory(source_dir)
    clean_up_directory(http_dir)
    logging.info('Roblox client has closed. Exiting...')
    print('Roblox client has closed. Exiting...')