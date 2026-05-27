# 🔮 AI Palm Reader

A mystical AI-powered palm reading application that analyzes palm images using vision language models. Upload a photo or capture one with your camera, and receive an instant, personalized palm reading with poetic insights about your personality, life path, emotional nature, and future opportunities — all in both English and Turkish.

🌐 **Live Demo**: [palm-reader-ai.streamlit.app](https://palm-reader-ai.streamlit.app/)

**How it works**: A vision-capable LLM (via LiteLLM) examines the image, the Instructor library enforces a structured output (suitability check + bilingual text), and the result is rendered in a clean Streamlit interface.

## 🚀 Local Development

### Prerequisites

- Python 3.12+
- API key from any LiteLLM-supported provider (OpenAI, Anthropic, Google, etc.)

### Setup & Run

```bash
# Clone
git clone https://github.com/YasinEfeee/Palm-Reader.git
cd Palm-Reader

# Install — choose one:
uv sync                    # recommended (fast)
# or
pip install -r requirements.txt   # fallback

# Configure credentials
# Create .streamlit/secrets.toml with:
#   LLM_API_KEY = "your_key_here"
#   LLM_MODEL  = "gemini/gemini-3.1-flash-lite"   # any vision-capable model

# Start the app — choose one:
uv run streamlit run src/main.py       # with uv
# or
streamlit run src/main.py              # with pip
```

Open `http://localhost:8501` in your browser. Uploads are limited to 20 MB.

### Supported Models

Any vision-capable model from LiteLLM's provider catalog is compatible.

## ☁️ Deploy to Streamlit Community Cloud

1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub, and click **New app**
3. Select your repo, set **Main file path** to `src/main.py`, and click **Deploy**
4. Go to app **Settings → Secrets** and add:

   ```toml
   LLM_API_KEY = "your_key_here"
   LLM_MODEL  = "gemini/gemini-3.1-flash-lite"
   ```

   The `gemini/gemini-3.1-flash-lite` model is recommended because it is fast and has a free tier on AI Studio. You can grab an API key from [AI Studio](https://aistudio.google.com/api-keys) and use it.

5. The app will auto-rebuild on every push to the deployed branch
