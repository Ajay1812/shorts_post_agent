from utils.Youtube.upload_shorts import UploadShorts, YoutubeShortsUploader
from utils.Youtube.textToSpeech import TTS
from utils.Youtube.generate_subtitles import Subtitles
from utils.Youtube.generate_final_video import FinalShort
from utils.Youtube.random_background_video import RandomVideo
from utils.processed_clip import ProcesseVideo
from workflows.shorts_workflow import workflow
import os
if __name__ == "__main__":
    agent = workflow()
    initial_state = {
        "user_topic": input("Enter your topic: "),
        "script": "",
        "yt_title": "",
        "yt_description":"",
        "yt_tags": [],
        "iteration": 1,
        "max_iteration": 3,
        "evaluation": "",
        "feedback": "",
        "feedback_history": []
    }
    result = agent.invoke(initial_state)
    # print(result["script"])
    # print(result)
    
    # Save script
    script_file = result["user_topic"].replace(" ", "_")
    with open(f"Data/scripts/{script_file}.txt", 'w') as f:
        f.write(result["script"])

    # Generate Audio
    output_audio_path = "Data/audio"
    process_tts = TTS(output_audio_path)
    process_tts.text_to_speech(script=result["script"], topic=result["user_topic"])
    
    # Generate Subtitles
    audio_file = f"{output_audio_path}/{result['user_topic'].replace(' ','_')}.wav"
    output_subtitles_path = "Data/subtitles"
    generate_subtitles = Subtitles(state=result)
    generate_subtitles.generate(audio_file=audio_file, subtitle_output_path=output_subtitles_path)
    subtitle_file = f"{output_subtitles_path}/{result['user_topic'].replace(' ', '_')}.srt"
    
    # Process raw video
    input_video_path = "Data/Raw/minecraft.mp4"
    output_path = "Data/processed_clips"
    process_clip = ProcesseVideo(input_video_path)
    process_clip.process(output_path)
    
    # Merge video + audio + subtitles
    final_output_path = "Data/upload"
    random_video = RandomVideo().select_random_video()
    video_file_path = f"Data/processed_clips/{random_video}"
    final_process = FinalShort(state=result)
    final_process.process(
        video_file_path=video_file_path,
        audio_file_path=audio_file,
        subtitle_file_path=subtitle_file,
        temp_path="Data/upload/temp.mp4",
        upload_shorts_path=final_output_path
    )

    client_secrets_file = "config/client.json"
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    uploader_auth = UploadShorts(client_secrets_file, scopes)
    youtube_client = uploader_auth.authenticate()

    uploader = YoutubeShortsUploader(youtube_client)
    uploader.upload_video(
        file_path=f"{final_output_path}/{result["user_topic"].replace(' ', '_')}.mp4",
        title=result["yt_title"],
        description=result["yt_description"],
        tags=result["yt_tags"],
        privacy_status="private"
    )