import whisper
import srt
from datetime import timedelta

class Subtitles:
    def __init__(self, state):
        self.model = whisper.load_model("base")
        self.file_name = state["user_topic"].replace(" ", "_")
    
    def generate(self, audio_file: str, subtitle_output_path: str):
        print(f"Audio Path: {audio_file}")
        try:
            subs = []
            response = self.model.transcribe(audio_file, fp16=False)
            for i, seg in enumerate(response["segments"], start=1):
                start = timedelta(seconds=seg["start"])
                end = timedelta(seconds=seg["end"])
                text = seg["text"].strip()
                subs.append(srt.Subtitle(index=i, start=start, end=end,content=text))
            with open(f"{subtitle_output_path}/{self.file_name}.srt", "w", encoding="utf-8") as f:
                f.write(srt.compose(subs))
                print(f"Subtiles stored: {subtitle_output_path}")
        except Exception as e:
            print(f"Error: {str(e)}")




