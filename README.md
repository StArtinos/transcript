# Transcript CLI for Windows

Split large audio files into 10-minute chunks, upload each chunk to the [Soniox](https://soniox.com) API, and download diarized transcripts — all from a single Python script (@transcript.py#1-205).

## Features

1. **Automatic chunking:** Long recordings are split into 10-minute MP3 segments before uploading (@transcript.py#41-55, @transcript.py#162-188).
2. **Speaker-aware transcription:** Each chunk is transcribed with speaker diarization enabled so you can see “Speaker 0/1/…” labels in the resulting text (@transcript.py#71-139, @transcript.py#142-159).
3. **Safe cleanup:** Uploaded files and transcription jobs are deleted from Soniox when processing finishes (@transcript.py#109-158).

## Prerequisites (Windows 10/11)

- 64-bit **Python 3.10+** installed via the Microsoft Store or python.org.
- **PowerShell** (ships with Windows 10/11).
- A **Soniox API key** (create a free account at <https://console.soniox.com/signup>).
- **FFmpeg + LAME** binaries available on your `PATH` so `pydub` can read/write audio.  
  - Fastest option: install via [winget](https://learn.microsoft.com/windows/package-manager/winget/) → `winget install Gyan.FFmpeg`.
  - Manual option: download a build from <https://www.gyan.dev/ffmpeg/builds/> and add the `bin` folder to your `PATH`.

## 1. Get the project onto the target PC

```powershell
# PowerShell
git clone https://github.com/<your_org>/Transcript.git
cd Transcript
```

> If you received the project as a ZIP, unzip it anywhere (e.g., `C:\Tools\Transcript`) and open PowerShell in that folder.

## 2. Create and activate a virtual environment

```powershell
py -3.11 -m venv .venv        # or: python -m venv .venv
.venv\Scripts\Activate.ps1    # use Activate.bat if running from cmd.exe
python -m pip install --upgrade pip
pip install requests python-dotenv pydub
```

These are the only runtime dependencies required by `transcript.py`. The script uses:

- `requests` for HTTPS calls,
- `python-dotenv` to load environment variables,
- `pydub` (backed by FFmpeg) for audio slicing (@transcript.py#8-54).

## 3. Provide your Soniox API key

Create a `.env` file in the project root with your API key:

```powershell
"SONIOX_API_KEY=<your_key_here>" | Out-File -Encoding utf8 .env
```

The script loads `.env` automatically (`load_dotenv()`), so every time you run the CLI your key is available (@transcript.py#23-37). **Never commit `.env` to version control.**

## 4. Run the CLI

From the activated virtual environment:

```powershell
python transcript.py "C:\path\to\meeting.mp3"
```

What happens:

1. Audio is split into `meeting_chunks\meeting_part_000.mp3`, `meeting_part_001.mp3`, … in the same folder as the original file.
2. Each chunk is uploaded, transcribed with speaker diarization, and saved as `meeting_transcripts\meeting_part_000.txt`, etc.
3. All results are printed to the console with basic progress information (@transcript.py#162-188).

You can adjust `CHUNK_MINUTES` in the script if you prefer longer/shorter segments (@transcript.py#19-55).

## 5. (Optional) Install the `transcript` command

Windows users can wrap the script with the provided batch file:

1. Ensure the virtual environment you created contains the dependencies.
2. Add `<repo>\transcript_bin` to your `PATH`.
3. Run `transcript <audio_file>` from any PowerShell/Command Prompt — the batch file calls the Python interpreter inside the project’s `venv` (@transcript_bin/transcript.cmd#1-2).

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `Missing SONIOX_API_KEY` | Confirm `.env` is present and contains `SONIOX_API_KEY=<value>`; restart the shell after editing. |
| `Couldn’t find ffmpeg` or MP3 export failures | Install FFmpeg/LAME and restart your terminal so the new `PATH` is loaded. |
| SSL / proxy errors on corporate networks | Set `REQUESTS_CA_BUNDLE` or configure your proxy per corporate IT guidelines. |
| Need to re-run without re-uploading | Delete the chunk folders and rerun; the script re-uploads from scratch each time. |

## Updating to a new release

1. Pull the latest code: `git pull`.
2. Re-activate the venv.
3. Reinstall dependencies if `requirements` change: `pip install -U requests python-dotenv pydub`.

You’re now ready to generate diarized transcripts on any Windows 10/11 machine.
