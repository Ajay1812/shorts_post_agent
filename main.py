from utils.Youtube.upload_shorts import UploadShorts, YoutubeShortsUploader
from utils.processed_clip import ProcesseVideo
from workflows.shorts_workflow import workflow

if __name__ == "__main__":
    agent = workflow()
    initial_state = {
        "user_topic": "What are the key differnces in OLAP vs OLTP systems?",
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
    
    input_video_path = "Data/Raw/minecraft.mp4"
    output_path = "Data/processed_clips"

    process_clip = ProcesseVideo(input_video_path)
    process_clip.process(output_path)
    
    client_secrets_file = "config/client.json"
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    uploader_auth = UploadShorts(client_secrets_file, scopes)
    youtube_client = uploader_auth.authenticate()

    uploader = YoutubeShortsUploader(youtube_client)
    uploader.upload_video(
        file_path="Data/upload/test.mp4",
        title=result["yt_title"],
        description=result["yt_description"],
        tags=result["yt_tags"],
        privacy_status="private"
    )