from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import os

class UploadShorts:
    def __init__(self, client_secrets_file, scopes):
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.token_file = 'token.json'

    def authenticate(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file,
            self.scopes
        )
        credentials = flow.run_local_server(port=8080)

        youtube = build("youtube", "v3", credentials=credentials)
        return youtube


class YoutubeShortsUploader:
    def __init__(self, youtube):
        self.youtube = youtube

    def upload_video(self, file_path, title, description, tags, privacy_status):
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22" 
            },
            "status": {
                "privacyStatus": privacy_status,
                "madeForKids": True 
            }
        }

        media_file = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/*')

        upload_request = self.youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        )

        response = None
        while response is None:
            status, response = upload_request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")

        print("Upload complete!")
        return response
