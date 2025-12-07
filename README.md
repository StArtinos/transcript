# Transcript CLI for Windows

A command-line tool that splits large audio files into chunks, transcribes them using the [Soniox](https://soniox.com) API with speaker diarization, and saves the results as text files.

---

## Quick Install (One-Time Setup)

Follow these steps to install `transcript` as a permanent system command.

### Step 1: Install Prerequisites

#### Python 3.10+

Download and install from [python.org](https://www.python.org/downloads/).

> **Important:** Check ✅ **"Add Python to PATH"** during installation.

Verify:
```powershell
python --version
```

#### FFmpeg

Open PowerShell and run:
```powershell
winget install Gyan.FFmpeg
```

Then **close and reopen PowerShell**.

Verify:
```powershell
ffmpeg -version
```

#### Soniox API Key

1. Create a free account at [console.soniox.com](https://console.soniox.com/signup).
2. Copy your API key from the dashboard.

---

### Step 2: Download & Install the Script

#### Option A: Using Git
```powershell
git clone https://github.com/StArtinos/transcript.git C:\Tools\Transcript
```

#### Option B: Manual Download
1. Download the ZIP from GitHub.
2. Extract to `C:\Tools\Transcript`.

---

### Step 3: Set Up Python Environment

Open PowerShell and run:

```powershell
cd C:\Tools\Transcript

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\Activate.ps1

# Install dependencies
pip install requests python-dotenv pydub
```

> **Permission error?** Run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

### Step 4: Configure Your API Key

Create the `.env` file with your Soniox API key:

```powershell
cd C:\Tools\Transcript
"SONIOX_API_KEY=your_api_key_here" | Out-File -Encoding utf8 .env
```

Replace `your_api_key_here` with your actual key.

---

### Step 5: Add to System PATH

This makes `transcript` available from any directory.

1. Press `Win + R`, type `sysdm.cpl`, press Enter.
2. Click **Advanced** tab → **Environment Variables**.
3. Under **System variables**, select `Path` → click **Edit**.
4. Click **New** and add:
   ```
   C:\Tools\Transcript\transcript_bin
   ```
5. Click **OK** on all dialogs.
6. **Close and reopen PowerShell**.

---

### Step 6: Update the Batch File Path

Edit `C:\Tools\Transcript\transcript_bin\transcript.cmd` to match your installation:

```cmd
@echo off
"C:\Tools\Transcript\venv\Scripts\python.exe" "C:\Tools\Transcript\transcript.py" %*
```

> If you installed to a different folder, update both paths accordingly.

---

## Usage

From **any directory** in PowerShell or Command Prompt:

```powershell
transcript "C:\path\to\audio.mp3"
```

### What It Does

1. Splits audio into 10-minute chunks → `<filename>_chunks\`
2. Uploads each chunk to Soniox for transcription
3. Saves transcripts with speaker labels → `<filename>_transcripts\`

### Example

```powershell
transcript "C:\Users\Me\meeting.mp3"
```

Output:
```
Splitting into 10-minute chunks...
Created 3 chunk(s) in: C:\Users\Me\meeting_chunks
Transcribing meeting_part_000.mp3...
  Uploading meeting_part_000.mp3...
  Creating transcription...
  Waiting for transcription...
  -> Saved transcript to C:\Users\Me\meeting_transcripts\meeting_part_000.txt
...
All transcripts saved in: C:\Users\Me\meeting_transcripts
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `'transcript' is not recognized` | Restart PowerShell. Verify `C:\Tools\Transcript\transcript_bin` is in your PATH. |
| `'python' is not recognized` | Reinstall Python with "Add to PATH" checked. Restart PowerShell. |
| `Couldn't find ffmpeg` | Run `winget install Gyan.FFmpeg` and restart PowerShell. |
| `Missing SONIOX_API_KEY` | Check `.env` exists in `C:\Tools\Transcript` with your API key. |
| `cannot be loaded because running scripts is disabled` | Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |

---

## Uninstall

1. Remove `C:\Tools\Transcript\transcript_bin` from your system PATH.
2. Delete the `C:\Tools\Transcript` folder.

---

## Configuration

Edit `transcript.py` to change settings:

```python
CHUNK_MINUTES = 10  # Audio chunk duration (default: 10 minutes)
```

---

## Supported Formats

MP3, WAV, OGG, FLAC, M4A, and any format FFmpeg supports.
