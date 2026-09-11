import os
import shutil
import subprocess

# Homebrew's plain `ffmpeg` formula is built without libass, so the `subtitles`
# filter is missing. The keg-only `ffmpeg-full` formula has it but is not on PATH.
FFMPEG_CANDIDATES = (
    os.environ.get("FFMPEG_BINARY"),
    "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg",
    "/usr/local/opt/ffmpeg-full/bin/ffmpeg",
    shutil.which("ffmpeg"),
)


def _has_subtitles_filter(binary: str) -> bool:
    result = subprocess.run(
        [binary, "-hide_banner", "-filters"], capture_output=True, text=True
    )
    return any(
        line.split()[1:2] == ["subtitles"] for line in result.stdout.splitlines()
    )


def _resolve_ffmpeg() -> str:
    fallback = None
    for candidate in FFMPEG_CANDIDATES:
        if not candidate or not os.path.exists(candidate):
            continue
        if _has_subtitles_filter(candidate):
            return candidate
        fallback = fallback or candidate
    if fallback:
        raise RuntimeError(
            f"{fallback} has no 'subtitles' filter (built without libass). "
            "Install a build that has it: brew install ffmpeg-full"
        )
    raise RuntimeError("ffmpeg not found")


def _escape_filter_value(value: str) -> str:
    """Escape a value for use inside an ffmpeg filter argument."""
    for char in ("\\", ":", ",", "'", "[", "]", ";"):
        value = value.replace(char, "\\" + char)
    return value


SUBTITLE_STYLE = (
    "FontName=Roboto,FontSize=12,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,"
    "BorderStyle=3,Outline=3,Shadow=2,Alignment=2,MarginV=60"
)

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
        ffmpeg = _resolve_ffmpeg()
        
        command = [
            ffmpeg, "-y",
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
            ffmpeg, "-y",
            "-i", temp_path,
            "-filter_complex",
            (
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=-0.2:saturation=0.8[bg];"
                "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
                "[bg][fg]overlay=(W-w)/2:(H-h)/2,"
                f"subtitles=filename={_escape_filter_value(subtitle_file_path)}"
                f":force_style={_escape_filter_value(SUBTITLE_STYLE)}"
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