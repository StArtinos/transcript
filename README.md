# Transcript CLI

A command-line tool that splits large audio files into chunks, transcribes them using the [Soniox](https://soniox.com) API with speaker diarization, and saves the results as text files.

Supports **Windows** and **Debian/Ubuntu Linux**.

---

## Prerequisites

Before installing, ensure you have:

- **Python 3.10+**
- **FFmpeg**
- **Soniox API Key** - Get one free at [console.soniox.com](https://console.soniox.com/signup)

---

## Windows Installation

### Step 1: Install Prerequisites

#### Python 3.10+

Download and install from [python.org](https://www.python.org/downloads/).

> **Important:** Check ✅ **"Add Python to PATH"** during installation.

Verify:
```powershell
python --version
```

#### FFmpeg

```powershell
winget install Gyan.FFmpeg
```

Restart PowerShell, then verify:
```powershell
ffmpeg -version
```

---

### Step 2: Download the Project

#### Option A: Using Git
```powershell
git clone https://github.com/StArtinos/transcript.git C:\Tools\Transcript
```

#### Option B: Manual Download
1. Download the ZIP from GitHub.
2. Extract to `C:\Tools\Transcript`.

---

### Step 3: Run the Installer

```powershell
cd C:\Tools\Transcript
.\install.bat
```

This will:
- Create a virtual environment
- Install Python dependencies
- Update `transcript.cmd` with correct paths

---

### Step 4: Configure Your API Key

Create the `.env` file:

```powershell
cd C:\Tools\Transcript
"SONIOX_API_KEY=your_api_key_here" | Out-File -Encoding utf8 .env
```

Replace `your_api_key_here` with your actual key.

---

### Step 5: Add to System PATH

1. Press `Win + R`, type `sysdm.cpl`, press Enter.
2. Click **Advanced** tab → **Environment Variables**.
3. Under **System variables**, select `Path` → click **Edit**.
4. Click **New** and add:
   ```
   C:\Tools\Transcript\transcript_bin
   ```
5. Click **OK** on all dialogs.
6. **Restart PowerShell**.

---

## Debian/Ubuntu Linux Installation

### Step 1: Install Prerequisites

```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install -y python3 python3-pip python3-venv

# Install FFmpeg
sudo apt install -y ffmpeg

# Verify installations
python3 --version
ffmpeg -version
```

---

### Step 2: Download the Project

#### Option A: Using Git
```bash
git clone https://github.com/StArtinos/transcript.git ~/Tools/Transcript
```

#### Option B: Manual Download
```bash
mkdir -p ~/Tools
cd ~/Tools
# Download and extract ZIP, then rename to Transcript
```

---

### Step 3: Set Up Python Environment

```bash
cd ~/Tools/Transcript

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install requests python-dotenv pydub
```

---

### Step 4: Configure Your API Key

```bash
cd ~/Tools/Transcript
echo "SONIOX_API_KEY=your_api_key_here" > .env
```

Replace `your_api_key_here` with your actual key.

---

### Step 5: Create the CLI Command

Create a shell script:

```bash
sudo tee /usr/local/bin/transcript > /dev/null << 'EOF'
#!/bin/bash
~/Tools/Transcript/venv/bin/python ~/Tools/Transcript/transcript.py "$@"
EOF

sudo chmod +x /usr/local/bin/transcript
```

> **Note:** If you installed to a different directory, update the paths in the script above.

Alternatively, add an alias to your `~/.bashrc`:

```bash
echo 'alias transcript="~/Tools/Transcript/venv/bin/python ~/Tools/Transcript/transcript.py"' >> ~/.bashrc
source ~/.bashrc
```

---

## Usage

From any directory:

**Windows:**
```powershell
transcript "C:\path\to\audio.mp3"
```

**Linux:**
```bash
transcript "/path/to/audio.mp3"
```

### What It Does

1. Splits audio into 10-minute chunks → `<filename>_chunks/`
2. Uploads each chunk to Soniox for transcription
3. Saves transcripts with speaker labels → `<filename>_transcripts/`

### Example

```bash
transcript ~/recordings/meeting.mp3
```

Output:
```
Splitting into 10-minute chunks...
Created 3 chunk(s) in: /home/user/recordings/meeting_chunks
Transcribing meeting_part_000.mp3...
  Uploading meeting_part_000.mp3...
  Creating transcription...
  Waiting for transcription...
  -> Saved transcript to /home/user/recordings/meeting_transcripts/meeting_part_000.txt
...
All transcripts saved in: /home/user/recordings/meeting_transcripts
```

---

## Troubleshooting

### Windows

| Error | Solution |
|-------|----------|
| `'transcript' is not recognized` | Restart PowerShell. Verify PATH includes `transcript_bin`. |
| `'python' is not recognized` | Reinstall Python with "Add to PATH" checked. |
| `Couldn't find ffmpeg` | Run `winget install Gyan.FFmpeg` and restart PowerShell. |
| `Missing SONIOX_API_KEY` | Check `.env` exists with your API key. |
| `scripts is disabled` | Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |

### Linux

| Error | Solution |
|-------|----------|
| `transcript: command not found` | Check `/usr/local/bin/transcript` exists or reload `~/.bashrc`. |
| `python3: command not found` | Run `sudo apt install python3`. |
| `ffmpeg: command not found` | Run `sudo apt install ffmpeg`. |
| `Missing SONIOX_API_KEY` | Check `.env` exists in the project directory. |
| `Permission denied` | Run `chmod +x /usr/local/bin/transcript`. |

---

## Uninstall

### Windows
1. Remove `C:\Tools\Transcript\transcript_bin` from your system PATH.
2. Delete the `C:\Tools\Transcript` folder.

### Linux
```bash
sudo rm /usr/local/bin/transcript
rm -rf ~/Tools/Transcript
# If using alias, remove it from ~/.bashrc
```

---

## Configuration

Edit `transcript.py` to change settings:

```python
CHUNK_MINUTES = 10  # Audio chunk duration (default: 10 minutes)
```

---

## Supported Formats

MP3, WAV, OGG, FLAC, M4A, and any format FFmpeg supports.
