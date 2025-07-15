# Chrome Wallet Detector

This tool scans all Chrome profiles on your computer for installed crypto wallet browser extensions (such as MetaMask, Rabby, Phantom, Trust Wallet, etc.).

## Features
- Detects popular wallet extensions across all Chrome profiles
- Resolves extension names even if they use localization (_locales)
- Prints extension name, description, version, and profile
- Runs `importer.py` (if present in the same directory) before scanning

## Requirements
- Python 3.7+
- No extra dependencies (uses only the Python standard library)

## Usage
1. Place `chrome_wallet_detector.py` and (optionally) `importer.py` in the same directory.
2. Open a terminal in that directory.
3. Run:
   ```bash
   python chrome_wallet_detector.py
   ```
4. The script will print any detected wallet extensions and their details.

## Notes
- Works on Windows, macOS, and Linux (for Chrome/Chromium-based browsers)
- Only scans local Chrome user profiles on the current machine
- If `importer.py` exists in the same directory, it will be executed automatically at startup 
