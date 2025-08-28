import subprocess
import os

class FinalShort:
    def __init__(self, state):
        self.final_file =  state["user_topic"].replace(" ", "_")
    
    def process(self, video_file_path: str, audio_file_path:str ,subtitle_file_path: str, temp_path: str, upload_shorts_path:str):
        if not os.path.exists(video_file_path):
            raise FileNotFoundError(f"video not found: {video_file_path}")
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"audio not found: {audio_file_path}")
        if not os.path.exists(subtitle_file_path):
            raise FileNotFoundError(f"subtitles not found: {subtitle_file_path}")
        if not os.path.exists(upload_shorts_path):
            os.makedirs(upload_shorts_path)
        
        command = [
            "ffmpeg",
            "-i", video_file_path,
            "-i", audio_file_path,
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            temp_path
        ]
        subprocess.run(command, check=True)
        print(f"✅ Merged video saved as {temp_path}")
        final_output = os.path.join(upload_shorts_path, f"{self.final_file}.mp4")
        command_subs = [
            "ffmpeg",
            "-i", temp_path,
            "-filter_complex",
            (
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=-0.2:saturation=0.8[bg];"
                "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,"
                f"subtitles={subtitle_file_path}:force_style='FontName=Roboto,FontSize=12,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=3,Outline=3,Shadow=2,Alignment=2,MarginV=60'" \
            ),
            "-c:a", "copy",
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "fast",
            final_output
        ]
        subprocess.run(command_subs, check=True)
        print(f"✅ Final video with subtitles saved as {final_output}")
        os.remove(temp_path)
        print("✅ Temp video removed")
        return final_output