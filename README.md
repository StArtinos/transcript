# Transcript CLI for Windows

Split large audio files into 10-minute chunks, upload each chunk to the [Soniox](https://soniox.com) API, and download diarized transcripts — all from a single Python script (@transcript.py#1-205).

## Features

1. **Automatic chunking:** Long recordings are split into 10-minute MP3 segments before uploading (@transcript.py#41-55, @transcript.py#162-188).
2. **Speaker-aware transcription:** Each chunk is transcribed with speaker diarization enabled so you can see “Speaker 0/1/…” labels in the resulting text (@transcript.py#71-139, @transcript.py#142-159).
3. **Safe cleanup:** Uploaded files and transcription jobs are deleted from Soniox when processing finishes (@transcript.py#109-158).
4. **Cross-platform:** Works on Windows 10/11 with PowerShell or Command Prompt.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

### 1. Python 3.10 or later

**Windows 10/11 users:**

- **Option A (Recommended):** Install from the [Microsoft Store](https://apps.microsoft.com/store/detail/python-311/9NRWMJP3717K)
  - Search for "Python" and install the latest version (3.11 or 3.12).
  - Automatically added to `PATH`.

- **Option B:** Install from [python.org](https://www.python.org/downloads/)
  - Download the Windows installer.
  - **Important:** Check the box "Add Python to PATH" during installation.
  - Verify installation: Open PowerShell and run `python --version`.

### 2. Git (optional, but recommended)

If you plan to clone the repository:

- Download and install from [git-scm.com](https://git-scm.com/download/win).
- Verify: `git --version` in PowerShell.

### 3. FFmpeg and LAME

The `pydub` library requires FFmpeg to read and write audio files. **This is mandatory.**

**Option A (Fastest - Recommended):**

If you have [Windows Package Manager (winget)](https://learn.microsoft.com/windows/package-manager/winget/) installed:

```powershell
winget install Gyan.FFmpeg
```

After installation, **restart PowerShell** to reload your `PATH`.

**Option B (Manual):**

1. Download a build from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/).
   - Choose the "full" build (includes LAME for MP3 support).
2. Extract the ZIP to a folder (e.g., `C:\Tools\ffmpeg`).
3. Add the `bin` folder to your system `PATH`:
   - Open **Settings** → **System** → **About** → **Advanced system settings**.
   - Click **Environment Variables**.
   - Under "System variables," select `Path` and click **Edit**.
   - Click **New** and add `C:\Tools\ffmpeg\bin` (adjust path as needed).
   - Click **OK** and close all dialogs.
4. **Restart PowerShell** and verify: `ffmpeg -version`.

### 4. Soniox API Key

1. Go to [console.soniox.com/signup](https://console.soniox.com/signup) and create a free account.
2. Log in and navigate to the **API Keys** section.
3. Copy your API key (keep it secret — never share or commit it to version control).

## Installation Steps

### Step 1: Get the Project

**If you have Git:**

```powershell
git clone https://github.com/<your_org>/Transcript.git
cd Transcript
```

**If you received a ZIP file:**

1. Right-click the ZIP and select **Extract All**.
2. Choose a location (e.g., `C:\Tools\Transcript`).
3. Open PowerShell in that folder (Shift + Right-click → "Open PowerShell window here").

### Step 2: Create a Virtual Environment

A virtual environment isolates project dependencies from your system Python.

```powershell
# Create the virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1
```

**If you get a permission error:**

PowerShell may block script execution. Run this once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then retry the activation command above.

**If using Command Prompt (cmd.exe) instead of PowerShell:**

```cmd
.venv\Scripts\Activate.bat
```

After activation, your prompt should show `(.venv)` at the beginning.

### Step 3: Install Dependencies

With the virtual environment activated:

```powershell
python -m pip install --upgrade pip
pip install requests python-dotenv pydub
```

**What these packages do:**

- `requests` — Makes HTTPS calls to the Soniox API.
- `python-dotenv` — Loads environment variables from the `.env` file.
- `pydub` — Handles audio splitting and format conversion (requires FFmpeg).

### Step 4: Configure Your API Key

Create a `.env` file in the project root directory with your Soniox API key:

```powershell
"SONIOX_API_KEY=<your_api_key_here>" | Out-File -Encoding utf8 .env
```

**Example:**

```powershell
"SONIOX_API_KEY=sk_live_abc123def456" | Out-File -Encoding utf8 .env
```

The script automatically loads this file when it runs (@transcript.py#23-37). **Never commit `.env` to version control** — it's already in `.gitignore`.

### Step 5: Verify the Setup

Test that everything works:

```powershell
python transcript.py --help
```

Or run a quick test with a sample audio file:

```powershell
python transcript.py "C:\path\to\sample.mp3"
```

## Usage

### Basic Usage

With the virtual environment activated:

```powershell
python transcript.py "C:\path\to\meeting.mp3"
```

### What Happens

1. **Audio splitting:** The script splits your audio into 10-minute chunks and saves them in a `<filename>_chunks` folder.
2. **Uploading & transcription:** Each chunk is uploaded to Soniox, transcribed with speaker diarization enabled, and then deleted.
3. **Output:** Transcripts are saved as `.txt` files in a `<filename>_transcripts` folder, with speaker labels (e.g., "Speaker 0:", "Speaker 1:").

### Example Output

```
Splitting into 10-minute chunks...
Created 3 chunk(s) in: C:\Users\You\Documents\meeting_chunks
Transcribing meeting_part_000.mp3...
  Uploading meeting_part_000.mp3...
  Creating transcription...
  Waiting for transcription...
  -> Saved transcript to C:\Users\You\Documents\meeting_transcripts\meeting_part_000.txt
...
All transcripts saved in: C:\Users\You\Documents\meeting_transcripts
```

### Customizing Chunk Size

To change the chunk duration, edit `transcript.py`:

```python
CHUNK_MINUTES = 10  # Change to 5, 15, 20, etc.
```

Then save and re-run the script.

## Advanced: Install as a Global Command (Optional)

If you want to run `transcript` from anywhere without activating the virtual environment:

1. Ensure the virtual environment is set up and contains all dependencies.
2. Add the `transcript_bin` folder to your system `PATH`:
   - Open **Settings** → **System** → **About** → **Advanced system settings**.
   - Click **Environment Variables**.
   - Under "System variables," select `Path` and click **Edit**.
   - Click **New** and add the full path to `<repo>\transcript_bin` (e.g., `C:\Tools\Transcript\transcript_bin`).
   - Click **OK** and close all dialogs.
3. **Restart PowerShell** and verify: `transcript "C:\path\to\audio.mp3"`.

The batch file (`transcript.cmd`) automatically calls the Python interpreter inside the project's virtual environment.

## Troubleshooting

### Python not found

**Error:** `python: The term 'python' is not recognized`

**Solutions:**

- Verify Python is installed: `python --version`
- If not found, reinstall Python from [python.org](https://www.python.org/downloads/) and **check "Add Python to PATH"**.
- **Restart PowerShell** after installation.
- If you installed via Microsoft Store, try `py --version` instead.

### FFmpeg not found

**Error:** `Couldn't find ffmpeg` or `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solutions:**

- Verify FFmpeg is installed: `ffmpeg -version`
- If not found, install via `winget install Gyan.FFmpeg` or manually (see Prerequisites section).
- **Restart PowerShell** after installation to reload `PATH`.
- Check that `C:\Tools\ffmpeg\bin` (or your installation path) is in your system `PATH`.

### Virtual environment activation fails

**Error:** `cannot be loaded because running scripts is disabled on this system`

**Solution:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then retry activation:

```powershell
.venv\Scripts\Activate.ps1
```

### Missing SONIOX_API_KEY

**Error:** `Missing SONIOX_API_KEY. 1. Get your API key at https://console.soniox.com 2. Add to .env: SONIOX_API_KEY=<YOUR_API_KEY>`

**Solutions:**

- Verify `.env` exists in the project root: `Test-Path .env`
- Check the file contains your key: `Get-Content .env`
- If the key is missing or incorrect, update it:
  ```powershell
  "SONIOX_API_KEY=<your_correct_key>" | Out-File -Encoding utf8 .env
  ```
- **Restart PowerShell** after editing `.env`.

### SSL/TLS or proxy errors

**Error:** `SSL: CERTIFICATE_VERIFY_FAILED` or connection timeouts on corporate networks

**Solutions:**

- If behind a corporate proxy, configure it:
  ```powershell
  $env:REQUESTS_CA_BUNDLE = "C:\path\to\corporate\ca-bundle.crt"
  ```
- Contact your IT department for the correct certificate bundle path.
- Alternatively, disable SSL verification (not recommended for production):
  ```powershell
  $env:PYTHONHTTPSVERIFY = 0
  ```

### Transcription fails or times out

**Error:** `Transcription error: Unknown error` or the script hangs

**Solutions:**

- Check your Soniox account has available credits.
- Verify your API key is correct and active.
- Check your internet connection.
- Try with a smaller audio file first to isolate the issue.
- Review Soniox API status at [status.soniox.com](https://status.soniox.com).

### Need to re-run without re-uploading

If you want to re-process without uploading again:

1. Delete the `<filename>_chunks` folder.
2. Re-run the script — it will re-upload from scratch.

Alternatively, keep the chunks folder and manually re-run transcription on specific chunks.

## Updating to a New Release

1. Pull the latest code:
   ```powershell
   git pull
   ```

2. Activate the virtual environment:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Reinstall dependencies (in case they've changed):
   ```powershell
   pip install -U requests python-dotenv pydub
   ```

4. Test with a sample file to ensure everything works.

## Project Structure

```
Transcript/
├── transcript.py              # Main CLI script
├── transcript_bin/
│   └── transcript.cmd         # Batch wrapper for global command
├── .env                       # Your API key (not in version control)
├── .gitignore                 # Excludes .env and venv/
├── README.md                  # This file
└── venv/                      # Virtual environment (created by you)
```

## FAQ

**Q: Can I use this on macOS or Linux?**

A: The script itself is cross-platform, but the installation steps are Windows-specific. You can adapt the instructions for your OS (use `python3 -m venv venv` and `source venv/bin/activate` on Unix-like systems).

**Q: How long does transcription take?**

A: Depends on audio length and Soniox queue. A 10-minute chunk typically takes 1–5 minutes.

**Q: Can I adjust the chunk size?**

A: Yes, edit `CHUNK_MINUTES` in `transcript.py` (line 20).

**Q: What audio formats are supported?**

A: `pydub` supports MP3, WAV, OGG, FLAC, and more. FFmpeg handles the conversion.

**Q: Is my API key safe?**

A: The `.env` file is excluded from version control. Never share it or commit it to a repository.

## Support

For issues with the script, check the [Soniox API documentation](https://docs.soniox.com).

For Python or FFmpeg issues, consult their official documentation or community forums.

You're now ready to generate diarized transcripts on any Windows 10/11 machine!
