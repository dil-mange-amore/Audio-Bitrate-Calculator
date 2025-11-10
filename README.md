# Audio Bitrate Calculator

A simple desktop tool built with Python and Tkinter to calculate the average bitrate of audio files in a directory and estimate the potential size after re-encoding.

## Features

*   **Select a folder**: Browse and select a folder containing your audio files.
*   **Filter by file type**: Choose to scan for all supported audio types or select a specific one (`mp3`, `flac`, `wav`, `aac`, `ogg`, `m4a`).
*   **Calculate average bitrate**: The tool processes all audio files in the selected folder (and its subdirectories) to calculate the average bitrate across all files.
*   **View total size**: See the total disk space occupied by the scanned audio files.
*   **Estimate new size**: After scanning, you can enter a new target bitrate (in kbps) to estimate what the total size of your library would be if you re-encoded all the files.
*   **Modern UI**: A clean, modern interface with a dark theme.
*   **Cross-platform**: Should run on Windows, macOS, and Linux where Python and Tkinter are available.

## How to Use

### Prerequisites

*   Python 3.x
*   The `mutagen` library

### Installation

1.  **Clone the repository or download the `Audio Bitrate Calculator.py` file.**

2.  **Install the required Python package:**

    Open your terminal or command prompt and run:
    ```bash
    pip install mutagen
    ```

### Running the Application

Once the dependency is installed, you can run the application from your terminal:

```bash
python "Audio Bitrate Calculator.py"
```

Or simply double-click the `.py` file if your system is configured to run Python scripts.

## How It Works

The application scans the selected directory recursively for audio files. For each file, it reads the metadata to get its bitrate and duration using the `mutagen` library. It then calculates the average bitrate and total size.

The "Estimated New Size" is calculated based on the total duration of all scanned files and the new bitrate you provide. The formula is:

`New Size (MB) = (Total Duration (seconds) * New Bitrate (kbps)) / (8 * 1024)`

## Credits

*   Concept and design by amol.more@hotmail.com
*   Built with help from Microsoft Copilot
