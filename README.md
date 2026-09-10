# Shorts Post Agent

Shorts Post Agent is a Python-based tool that **automates the creation and publishing of YouTube Shorts videos.** Given a topic (pulled automatically from `Data/Raw/plan.md`), the agent generates a video **script using AI, converts it to speech, produces subtitles, merges the audio with a background video, and uploads the final short to YouTube.** The pipeline leverages modern AI models (LangChain, LangGraph agents, TTS (Kokoro or Pocket TTS), ASR (OpenAI’s Whisper)) and the YouTube Data API to create a complete end-to-end shorts workflow.

## Features

- **AI Script Generation:** Creates and refines scripts from a topic using an LLM workflow.

- **YouTube Metadata:** Generates titles, descriptions, and tags automatically.

- **Text-to-Speech (TTS):** Converts scripts into speech using a selectable engine — [Kokoro](https://github.com/hexgrad/kokoro) (default) or [Pocket TTS](https://kyutai.org/blog/2026-01-13-pocket-tts/) — with a choice of voice, via `--tts-engine`/`--voice`.

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

- The script will use this file to authenticate and upload the video using the youtube.upload scope.

- The first upload opens a browser window to log in and grant access; the resulting credentials are cached in `token.json` (git-ignored) and automatically refreshed on later runs, so you won't be asked to log in again unless `token.json` is deleted or the grant is revoked.

**4. .env file:**

```bash
GEMINI_API_KEY="enter_your_api_key"
GEMINI_PRO_API_KEY="enter_your_api_key"
```

**5. Verify FFmpeg:**
Whisper and the video processing require FFmpeg. Install it via your package manager (e.g., `sudo apt install ffmpeg)`. Without FFmpeg, subtitle generation will fail

**6. Prepare raw video:**
Place your background video(s) in `Data/Raw/`. You can use any MP4 video (vertical aspect recommended for Shorts).

**7. Run the pipeline:**

The topic is picked up automatically from the next unchecked item in `Data/Raw/plan.md` — there is no interactive prompt. The TTS engine, voice, and YouTube upload privacy can be selected via CLI flags:

```bash
# Default (Kokoro, voice af_bella, private upload)
$ python main.py

# Use Pocket TTS with a specific voice
$ python main.py --tts-engine pocket --voice alba

# Use Kokoro with a specific voice, publish publicly
$ python main.py --tts-engine kokoro --voice af_bella --privacy-status public

# See all options
$ python main.py --help
```

Supported `--tts-engine` values: `kokoro` (default voice `af_bella`), `pocket` (default voice `alba`; 20+ voices across English/Italian/Spanish/German/Portuguese/French, see the [Pocket TTS voice catalog](https://kyutai.org/blog/2026-01-13-pocket-tts/)).

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
│   ├── tts/
│   │   ├── base.py         # BaseTTS interface
│   │   ├── kokoro_tts.py    # Kokoro TTS engine
│   │   ├── pocket_tts.py    # Pocket TTS engine
│   │   └── factory.py      # build_tts(engine, voice, output_path)
│   └── Youtube/
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

## Automating with Cron (Linux/Mac)

You can schedule the Shorts Post Agent to run automatically every day using **cron**.

1. Find your Python path:
   ```bash
   which python3
   ```
2. Open the cron editor:

    ```bash
    crontab -e
    ```

3. Add a job to run the script every day at 5:00 PM:

    ```bash
    0 17 * * * /home/user_name/python_path/python/3.13.7/bin/python3 /home/nf/Documents/projects/shorts_post_agent/main.py >> /home/nf/cron.log 2>&1
    ```
- 0 17 * * * → Runs daily at 5:00 PM
- First path → Python interpreter
- Second path → Project’s main.py file
- **Logs:** /home/nf/cron.log 2>&1 → Saves logs & errors for debugging

4. Save and exit. Verify with:
    ```bash
    crontab -l
    ```
Now the Shorts Post Agent will run automatically every day at 5 PM 🎥✨