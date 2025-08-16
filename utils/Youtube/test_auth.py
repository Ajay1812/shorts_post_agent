from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    "/home/nf/Documents/Projects/shorts_post_agent/config/client.json",
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)

credentials = flow.run_local_server()
print("Access Token:", credentials.token)
