# 🎓 Personal Study Tutor AI

A sophisticated, context-aware AI tutor built with Streamlit and powered by LLMs. This tutor adapts its teaching style, difficulty, and explanations based on your skill level and past interactions.

## 🚀 Features

*   **Adaptive Learning**: Choose between Beginner, Intermediate, and Advanced levels. The tutor adjusts its language and complexity accordingly.
*   **Context Awareness**: Remembers your subject, skill level, and weak topics across the session.
*   **Interactive Chat**: A ChatGPT-like interface for deep learning sessions.
*   **Quiz System**: Generates personalized MCQs and short-answer questions to test your knowledge.
*   **Progress Tracking**: Tracks topics studied and quiz accuracy to help you monitor your growth.
*   **Multiple Teaching Modes**: Switch between 'Explain simply', 'Step-by-step', 'Exam mode', and 'Real-world examples'.

## 🛠️ Tech Stack

*   **Python**: Core logic.
*   **Streamlit**: Interactive web interface.
*   **OpenAI API**: Powering the cognitive engine (can be used with Ollama/Groq for open-source models).

## 📦 Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Provide API Key
Enter your OpenAI-compatible API key in the sidebar to start chatting with your personal tutor!

## 📂 Project Structure

```
study_tutor/
├── app.py          # Main Streamlit application
├── tutor.py        # LLM interaction & adaptive logic
├── memory.py       # Context & persistent storage
├── quiz.py         # Quiz generation & evaluation
├── prompts.py      # Structured prompt templates
├── utils.py        # UI components & styling
└── data/           # User data persistence
```
