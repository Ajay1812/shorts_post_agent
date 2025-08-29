# Shorts Post Agent

Shorts Post Agent is a Python-based tool that **automates the creation and publishing of YouTube Shorts videos.** Given a topic input, the agent generates a video **script using AI, converts it to speech, produces subtitles, merges the audio with a background video, and uploads the final short to YouTube.** The pipeline leverages modern AI models (LangChain, LangGraph agents, TTS (Kokoro), ASR (OpenAI’s Whisper), ) and the YouTube Data API to create a complete end-to-end shorts workflow.

## Features

- **AI Script Generation:** Creates and refines scripts from a topic using an LLM workflow.

- **YouTube Metadata:** Generates titles, descriptions, and tags automatically.

- **Text-to-Speech (TTS):** Converts scripts into speech using the Kokoro model.

- **Auto-Subtitles (ASR):** Transcribes audio into timed SRT subtitles with Whisper (requires FFmpeg).

- **Video Processing:** Cuts raw footage into clips and merges with audio + subtitles.

- **YouTube Upload:** Authenticates with YouTube Data API to upload Shorts (default: private).

- **Configurable Workflow:** Modular pipeline with customizable prompts and settings.

---

## Installation

**1. Clone the repository:**

```bash
git clone https://github.com/Ajay1812/shorts_post_agent.git
cd shorts_post_agent
```

**2. Create virtual environment & install dependencies using uv**

```bash
uv init
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
uv sync
```

💡 If you don’t have uv, install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**3. Set up Google credentials:**

- Go to the Google Cloud Console, enable the **YouTube Data V3 API,** and create **OAuth 2.0** credentials.

- Download the **client_secret.json** file and place it at **config/client.json**. Ensure it is named client.json or update main.py accordingly.

- The script will use this file to authenticate and upload the video using the youtube.upload scope

**4. .env file:**

```bash
GEMINI_API_KEY="enter_your_api_key"
GEMINI_PRO_API_KEY="enter_your_api_key"
```

**5. Verify FFmpeg:**
Whisper and the video processing require FFmpeg. Install it via your package manager (e.g., `sudo apt install ffmpeg)`. Without FFmpeg, subtitle generation will fail

**6. Prepare raw video:**
Place your background video(s) in `Data/Raw/`. You can use any MP4 video (vertical aspect recommended for Shorts).

**7. Run the main script and follow the prompt. For example:**

```bash
$ python main.py
Enter your topic: What are OLAP and OLTP systems?
```

---

## Project Structure

```
shorts_post_agent/
├── Data/                   # Storage for media and outputs
│   ├── Raw/                # Raw input videos (e.g. minecraft.mp4)
│   ├── audio/              # Generated WAV audio from TTS
│   ├── subtitles/          # Generated SRT subtitle files
│   ├── processed_clips/    # Video clips cut from raw video
│   ├── upload/             # Final videos ready for upload (final.mp4)
│   └── scripts/            # Generated script text files
├── config/
│   ├── client.json         # YouTube OAuth2 credentials (Google API)
│   └── settings.py         # Configuration loader (loads prompts from .env)
├── utils/
│   ├── llm.py              # LLM wrapper functions
│   ├── processed_clip.py   # Video splitting utilities
│   ├── script_generator.py # AI script generation logic
│   └── Youtube/
│       ├── textToSpeech.py      # Kokoro TTS interface
│       ├── generate_subtitles.py # Whisper ASR interface
│       ├── generate_final_video.py # Merging video/audio/subtitles
│       ├── upload_shorts.py      # YouTube upload helper
│       └── yt_info_generate.py   # Title/description/tag generation
├── workflows/
│   └── shorts_workflow.py  # Defines the AI agent workflow/graph
├── main.py                 # Entry point that runs the pipeline
├── pyproject.toml          # Project metadata and dependency listing
└── README.md
```
