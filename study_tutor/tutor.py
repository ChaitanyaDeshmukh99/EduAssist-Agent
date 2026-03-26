import openai
import os
import streamlit as st
from prompts import TUTOR_SYSTEM_PROMPT

class PersonalTutor:
    def __init__(self, api_key=None, model="mistralai/Mistral-7B-Instruct-v0.2"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
        
        # Safely try to get from Streamlit secrets
        if not self.api_key:
            try:
                self.api_key = st.secrets.get("HF_TOKEN") or st.secrets.get("OPENAI_API_KEY")
            except FileNotFoundError:
                self.api_key = None
        
        self.model = model
        self.client = None
        
        if self.api_key:
            if self.api_key.startswith("hf_"):
                # Hugging Face Inference API (OpenAI-compatible)
                self.client = openai.OpenAI(
                    base_url="https://router.huggingface.co/hf-inference/v1/",
                    api_key=self.api_key
                )
            elif self.api_key.startswith("AIza"):
                # Google Gemini API (OpenAI-compatible)
                self.client = openai.OpenAI(
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                    api_key=self.api_key
                )
            else:
                # Standard OpenAI
                self.client = openai.OpenAI(api_key=self.api_key)

    def generate_response(self, user_input, chat_history, profile):
        """Generates a personalized tutor response based on history and profile."""
        if not self.client:
            return "⚠️ LLM API Key not found. Please provide an API key in the sidebar or environment variables to enable the tutor."

        system_prompt = TUTOR_SYSTEM_PROMPT.format(
            subject=profile.get("subject", "General"),
            skill_level=profile.get("skill_level", "Beginner"),
            teaching_mode=profile.get("teaching_mode", "Explain simply"),
            weak_topics=", ".join(profile.get("weak_topics", [])) or "None identified yet"
        )

        messages = [{"role": "system", "content": system_prompt}]
        
        # Add relevant chat history (last 5-10 turns)
        for msg in chat_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"

    def analyze_weakness(self, chat_history):
        """Optional: Periodically analyze chat history to detect weak topics."""
        # This could be a separate call to the LLM to summarize difficulties
        pass
