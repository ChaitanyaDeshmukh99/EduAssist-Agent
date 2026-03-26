# 🎓 Personal Study Tutor AI

A sophisticated, context-aware AI tutor built with Streamlit and powered by advanced LLMs via NVIDIA NIM and OpenAI-compatible interfaces. This tutor adapts its teaching style, effortlessly handles multi-modal images and massive PDF context uploads, and creates visual study aids on demand.

## 🚀 Features
*   **Multi-Model Support**: Defaults to NVIDIA's extraordinarily powerful `meta/llama3-70b-instruct` and `meta/llama-3.2-90b-vision-instruct` models for text and image analysis.
*   **Multimodal Vision**: Upload screenshots of code, math problems, or diagrams directly into the chat for logical evaluation.
*   **NotebookLM-style Research (RAG)**: Attach massive PDF or TXT files to inject custom context straight into the LLM's brain for flawless, cited answers.
*   **AI Image Studio**: A dedicated generation studio allowing you to prompt high-resolution visual study aids directly into your chat trace using NVIDIA's Stability APIs.
*   **Study Guide Exporter**: Automatically synthesizes your entire chat session and uploaded documents into a pristine, beautifully structured Markdown study guide ready for PDF export.
*   **Premium Dark Mode UI**: Completely custom glassmorphism components with radial gradients, glowing buttons, and bespoke typography.

## 🛠️ Tech Stack
*   **Python**: Core application logic.
*   **Streamlit**: Highly-customized native web layout.
*   **OpenAI SDK (`openai`)**: Universal API adapter querying NVIDIA NIM, Google Gemini, Hugging Face Serverless, and OpenAI endpoints.
*   **PyPDF2**: Native robust PDF context extraction.
*   **python-dotenv**: Environment variable management for optimal security.

## 📦 Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed and clone the repository locally.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the root directory and securely configure your API instances (specifically NVIDIA for full feature support):
```env
NVIDIA_API_KEY="nvapi-..."
GEMINI_API_KEY="AIza..."
HF_TOKEN="hf_..."
OPENAI_API_KEY="sk-..."
```
*(The `.gitignore` strictly protects this file from being pushed to public versions of your repo)*

### 4. Run the App
```bash
streamlit run app.py
```

## 📂 Project Structure
```text
study_tutor/
├── app.py          # Main Streamlit UI, visual routing, & tab integrations
├── tutor.py        # OpenAI SDK wrapper, raw SD3 HTTP hooks, and Model routing logic
├── memory.py       # Context arrays & persistent storage for user profiles
├── prompts.py      # Core LLM prompt templates and behavior controls
├── utils.py        # UI extraction helpers, massive CSS payload, & native tweaks
├── data/           # User data JSON persistence
└── .env            # Secure API Keys (not tracked by Git)
```
