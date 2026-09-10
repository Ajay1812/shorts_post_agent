from utils.tts.base import BaseTTS

SUPPORTED_ENGINES = ("kokoro", "pocket")


def build_tts(engine: str, voice: str | None, output_path: str) -> BaseTTS:
    if engine == "kokoro":
        from utils.tts.kokoro_tts import KokoroTTS, DEFAULT_VOICE

        return KokoroTTS(output_path, voice or DEFAULT_VOICE)
    elif engine == "pocket":
        from utils.tts.pocket_tts import PocketTTS, DEFAULT_VOICE

        return PocketTTS(output_path, voice or DEFAULT_VOICE)
    else:
        raise ValueError(
            f"Unknown TTS engine '{engine}'. Supported engines: {', '.join(SUPPORTED_ENGINES)}"
        )
