"""Simple Realtime API demo: record microphone audio, get text reply."""

import asyncio
import base64
import json
import os
from typing import Optional

import sounddevice as sd
import websockets


REALTIME_URL = "wss://api.openai.com/v1/realtime"
SAMPLE_RATE = 16000
CHUNK_MS = 200


def record_audio(duration: float) -> bytes:
    frames = int(SAMPLE_RATE * duration)
    if frames <= 0:
        raise ValueError("duration must be positive")

    recording = sd.rec(frames, samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()
    audio_bytes = recording.tobytes()
    if not audio_bytes:
        raise RuntimeError("microphone produced no audio; check input device or permissions")
    return audio_bytes


async def stream_audio_and_get_text(
    audio_pcm: bytes,
    *,
    model: str,
    instructions: str,
    temperature: Optional[float] = None,
) -> str:
    openai_api_key = os.environ["OPENAI_API_KEY"]
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "OpenAI-Beta": "realtime=v1"
    }

    url = f"{REALTIME_URL}?model={model}"
    async with websockets.connect(url, additional_headers=headers) as ws:
        await ws.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "instructions": instructions,
                        "modalities": ["text"],
                        "input_audio_format": "pcm16",
                        **({"temperature": temperature} if temperature is not None else {}),
                    },
                }
            )
        )

        chunk_bytes = int(SAMPLE_RATE * (CHUNK_MS / 1000) * 2)
        for start in range(0, len(audio_pcm), chunk_bytes):
            chunk = audio_pcm[start : start + chunk_bytes]
            if not chunk:
                continue
            await ws.send(
                json.dumps(
                    {
                        "type": "input_audio_buffer.append",
                        "audio": base64.b64encode(chunk).decode("ascii"),
                    }
                )
            )

        await ws.send(json.dumps({"type": "input_audio_buffer.commit"}))

        await ws.send(
            json.dumps(
                {
                    "type": "response.create",
                    "response": {
                        "modalities": ["text"],
                        "instructions": "Listen to the committed audio and reply in concise text.",
                    },
                }
            )
        )

        text = []
        async for message in ws:
            payload = json.loads(message)
            match payload.get("type"):
                case "response.output_text.delta":
                    text.append(payload["delta"])
                case "response.completed":
                    break
                case "error":
                    raise RuntimeError(payload)

        return "".join(text).strip()


async def main() -> None:
    duration = float(os.getenv("REALTIME_RECORD_SECONDS", "4"))
    model = os.getenv("REALTIME_MODEL", "gpt-4o-realtime-preview")
    prompt = os.getenv(
        "REALTIME_SYSTEM_PROMPT",
        "The user will speak Japanese. Reply in Japanese text with a short summary.",
    )

    print(f"Recording {duration} seconds of audio...")
    pcm16 = record_audio(duration)

    print("Sending audio to Realtime API...")
    reply = await stream_audio_and_get_text(pcm16, model=model, instructions=prompt)

    print("--- assistant reply ---")
    print(reply or "(no text received)")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted.")

