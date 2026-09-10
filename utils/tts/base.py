from abc import ABC, abstractmethod


class BaseTTS(ABC):
    """Common interface every TTS engine implementation must provide."""

    def __init__(self, output_path: str, voice: str):
        self.output_path = output_path
        self.voice = voice

    @abstractmethod
    def text_to_speech(self, script: str, topic: str) -> str:
        """Synthesize `script` to a WAV file under `output_path` and return a status message."""
        raise NotImplementedError
