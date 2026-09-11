import os
import whisper
import srt
from datetime import timedelta

class Subtitles:
    def __init__(self, state):
        self.model = whisper.load_model("base")
        self.file_name = state["user_topic"].replace(" ", "_")

    def generate(self, audio_file: str, subtitle_output_path: str):
        print(f"Audio Path: {audio_file}")
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"audio not found: {audio_file}")
        os.makedirs(subtitle_output_path, exist_ok=True)

        subs = []
        response = self.model.transcribe(audio_file, fp16=False)
        for i, seg in enumerate(response["segments"], start=1):
            start = timedelta(seconds=seg["start"])
            end = timedelta(seconds=seg["end"])
            text = seg["text"].strip()
            subs.append(srt.Subtitle(index=i, start=start, end=end, content=text))

        subtitle_file = os.path.join(subtitle_output_path, f"{self.file_name}.srt")
        with open(subtitle_file, "w", encoding="utf-8") as f:
            f.write(srt.compose(subs))
        print(f"Subtitles stored: {subtitle_file}")
        return subtitle_file
