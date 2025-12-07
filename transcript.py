"""
Transcript CLI - Split audio into chunks and transcribe with Soniox (speaker diarization enabled).

Usage:
    transcript <audio_file>
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional

import requests
from requests import Session
from dotenv import load_dotenv
from pydub import AudioSegment

# Configuration
CHUNK_MINUTES = 10
SONIOX_API_BASE_URL = "https://api.soniox.com"

# Load environment variables
load_dotenv()


def get_soniox_session() -> Session:
    """Create an authenticated Soniox API session."""
    api_key = os.environ.get("SONIOX_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing SONIOX_API_KEY.\n"
            "1. Get your API key at https://console.soniox.com\n"
            "2. Add to .env: SONIOX_API_KEY=<YOUR_API_KEY>"
        )
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {api_key}"
    return session


def split_audio(input_path: Path, output_dir: Path, chunk_minutes: int = CHUNK_MINUTES) -> list[Path]:
    """Split audio into fixed-length chunks and save them into output_dir."""
    audio = AudioSegment.from_file(input_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks: list[Path] = []
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        end = min(start + chunk_ms, len(audio))
        chunk = audio[start:end]

        chunk_path = output_dir / f"{input_path.stem}_part_{i:03d}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)

    return chunks


def upload_audio(session: Session, audio_path: Path) -> str:
    """Upload audio file to Soniox and return file_id."""
    print(f"  Uploading {audio_path.name}...")
    with audio_path.open("rb") as f:
        res = session.post(
            f"{SONIOX_API_BASE_URL}/v1/files",
            files={"file": f},
        )
    res.raise_for_status()
    file_id = res.json()["id"]
    return file_id


def create_transcription(session: Session, file_id: str) -> str:
    """Create a transcription job with speaker diarization enabled."""
    config = {
        "model": "stt-async-v3",
        "enable_speaker_diarization": True,
        "file_id": file_id,
    }
    res = session.post(
        f"{SONIOX_API_BASE_URL}/v1/transcriptions",
        json=config,
    )
    res.raise_for_status()
    return res.json()["id"]


def wait_until_completed(session: Session, transcription_id: str) -> None:
    """Poll until transcription is completed."""
    while True:
        res = session.get(f"{SONIOX_API_BASE_URL}/v1/transcriptions/{transcription_id}")
        res.raise_for_status()
        data = res.json()
        status = data["status"]
        if status == "completed":
            return
        elif status == "error":
            raise Exception(f"Transcription error: {data.get('error_message', 'Unknown error')}")
        time.sleep(2)


def get_transcription(session: Session, transcription_id: str) -> dict:
    """Fetch the transcription result."""
    res = session.get(
        f"{SONIOX_API_BASE_URL}/v1/transcriptions/{transcription_id}/transcript"
    )
    res.raise_for_status()
    return res.json()


def delete_transcription(session: Session, transcription_id: str) -> None:
    """Delete transcription from Soniox."""
    res = session.delete(f"{SONIOX_API_BASE_URL}/v1/transcriptions/{transcription_id}")
    res.raise_for_status()


def delete_file(session: Session, file_id: str) -> None:
    """Delete uploaded file from Soniox."""
    res = session.delete(f"{SONIOX_API_BASE_URL}/v1/files/{file_id}")
    res.raise_for_status()


def render_tokens(tokens: list[dict]) -> str:
    """Convert tokens into readable transcript with speaker labels."""
    text_parts: list[str] = []
    current_speaker: Optional[int] = None

    for token in tokens:
        text = token["text"]
        speaker = token.get("speaker")

        # Speaker changed -> add speaker label
        if speaker is not None and speaker != current_speaker:
            if current_speaker is not None:
                text_parts.append("\n\n")
            current_speaker = speaker
            text_parts.append(f"Speaker {current_speaker}:\n")

        text_parts.append(text)

    return "".join(text_parts).strip()


def transcribe_file(session: Session, audio_path: Path) -> str:
    """Upload, transcribe, and return text with speaker diarization."""
    file_id = upload_audio(session, audio_path)

    print(f"  Creating transcription...")
    transcription_id = create_transcription(session, file_id)

    print(f"  Waiting for transcription...")
    wait_until_completed(session, transcription_id)

    result = get_transcription(session, transcription_id)
    text = render_tokens(result.get("tokens", []))

    # Cleanup
    delete_transcription(session, transcription_id)
    delete_file(session, file_id)

    return text


def process_audio_file(audio_path: Path) -> None:
    """Split an audio file into chunks, transcribe each, and save txt files."""
    base_dir = audio_path.parent
    chunks_dir = base_dir / f"{audio_path.stem}_chunks"
    transcripts_dir = base_dir / f"{audio_path.stem}_transcripts"

    chunks_dir.mkdir(exist_ok=True)
    transcripts_dir.mkdir(exist_ok=True)

    print(f"Splitting into {CHUNK_MINUTES}-minute chunks...")
    chunks = split_audio(audio_path, chunks_dir)
    print(f"Created {len(chunks)} chunk(s) in: {chunks_dir}")

    # Create Soniox session
    session = get_soniox_session()

    for chunk in chunks:
        print(f"Transcribing {chunk.name}...")
        text = transcribe_file(session, chunk)

        txt_name = f"{chunk.stem}.txt"
        out_path = transcripts_dir / txt_name
        out_path.write_text(text, encoding="utf-8")
        print(f"  -> Saved transcript to {out_path}")

    print(f"\nAll transcripts saved in: {transcripts_dir}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: transcript <audio_file>")
        sys.exit(1)

    audio_path = Path(sys.argv[1]).resolve()

    if not audio_path.exists():
        print(f"File not found: {audio_path}")
        sys.exit(1)

    process_audio_file(audio_path)


if __name__ == "__main__":
    main()