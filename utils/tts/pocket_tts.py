from scipy.io import wavfile
from pocket_tts import TTSModel

from utils.tts.base import BaseTTS

DEFAULT_VOICE = "alba"
SAMPLE_RATE = 24000


class PocketTTS(BaseTTS):
    def __init__(self, output_path: str, voice: str = DEFAULT_VOICE):
        super().__init__(output_path, voice or DEFAULT_VOICE)
        self.model = TTSModel.load_model()

    def text_to_speech(self, script: str, topic: str) -> str:
        topic = topic.replace(" ", "_")
        voice_state = self.model.get_state_for_audio_prompt(self.voice)
        audio = self.model.generate_audio(voice_state, script)

        wavfile.write(f"{self.output_path}/{topic}.wav", SAMPLE_RATE, audio.numpy())
        return f"✅ Combined reel saved as {topic}.wav"
