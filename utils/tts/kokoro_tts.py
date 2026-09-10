import numpy as np
import soundfile as sf
from kokoro import KPipeline

from utils.tts.base import BaseTTS

DEFAULT_VOICE = "af_bella"
SAMPLE_RATE = 24000


class KokoroTTS(BaseTTS):
    def __init__(self, output_path: str, voice: str = DEFAULT_VOICE):
        super().__init__(output_path, voice or DEFAULT_VOICE)

    def text_to_speech(self, script: str, topic: str) -> str:
        topic = topic.replace(" ", "_")
        pipeline = KPipeline(lang_code="a")
        generator = pipeline(script, voice=self.voice)

        combined_audio = []
        for i, (gs, ps, audio) in enumerate(generator):
            print(i, gs, ps)
            combined_audio.append(audio)

        final_audio = np.concatenate(combined_audio)
        sf.write(f"{self.output_path}/{topic}.wav", final_audio, SAMPLE_RATE)
        return f"✅ Combined reel saved as {topic}.wav"
