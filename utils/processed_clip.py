import subprocess
import os
import glob

class ProcesseVideo:
    def __init__(self, input_path: str):
        self.input_path = input_path
    def process(self, output_path:str, part_duration=75):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input video not found: {self.input_path}")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        existing_parts = glob.glob(os.path.join(output_path, "part_*.mp4"))
        if existing_parts:
            print(f"Skipping split — found {len(existing_parts)} parts already in {output_path}")
            return
        
        output_template = os.path.join(output_path,  "part_%03d.mp4")
        command = [
            "ffmpeg",
            "-i", self.input_path,
            "-c", "copy",
            "-map", "0",
            "-f", "segment",
            "-segment_time", str(part_duration),
            "-reset_timestamps", "1",
            output_template
        ]
        print("Running FFmpeg command:")
        print(" ".join(command))
        try:
            subprocess.run(command, check=True)
            print(f"Video successfully split into {part_duration}-second clips at {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error splitting video: {e}")