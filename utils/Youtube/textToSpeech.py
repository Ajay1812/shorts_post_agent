from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import numpy as np

class TTS:
    def __init__(self, path):
        self.path = path

    def text_to_speech(self, script, topic):
        combined_audio = []
        topic = topic.replace(" ", "-")
        pipeline = KPipeline(lang_code='a')
        generator = pipeline(script, voice='af_bella')
        
        for i, (gs, ps, audio) in enumerate(generator):
            print(i, gs, ps)
            display(Audio(data=audio, rate=24000, autoplay=i==0))
            # sf.write(f'{i}.wav', audio, 24000)
            combined_audio.append(audio)
        final_audio = np.concatenate(combined_audio)
        sf.write(f"{self.path}/{topic}.wav", final_audio, 24000)
        return f"✅ Combined reel saved as {topic}.wav"