# Roblox Audio Capture

## Description

**Roblox Audio Capture** is a Python script designed to monitor the Roblox game client's temporary sound folder, automatically back up audio files, and rename them for easier access.

## Features

- Monitors the Roblox client’s folder for new audio files.
- Copies and renames audio files from `binary` to `.ogg` format.
- Deletes old files from the source directory before and after the monitoring session.
- Alerts users that audio files may work but might have issues with some audio players.
- Notes that the `.ogg` files do not retain their original asset names due to Roblox's encryption.

## Requirements

- Python 3.x
- `psutil` library
- `shutil` library

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Ghosty-Tongue/roblox-audio-capture.git
   ```

2. **Navigate to the repository directory:**

   ```bash
   cd roblox-audio-capture
   ```

3. **Install the required libraries:**

   ```bash
   pip install psutil
   ```

## Usage

1. **Run the script:**

   ```bash
   python audio.py
   ```

3. **Monitor the output**: The script will print messages about the status of file copying and renaming.

4. **Backup Directory**: The audio files will be copied to the `sound_backup` folder in your `Downloads` directory.

## Important Notes

- The `.ogg` files may not retain their original asset names because Roblox encrypts the original file names. This encryption makes it difficult to determine the original uploaded file name.
- While the audio files may work, some audio players might have difficulty playing them.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Roblox community for providing insights into audio handling within Roblox games.
