import openai
import os
import streamlit as st
import requests
from prompts import TUTOR_SYSTEM_PROMPT

class PersonalTutor:
    def __init__(self, api_key=None, model="meta/llama3-70b-instruct"):
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            try:
                self.api_key = st.secrets.get("HF_TOKEN") or st.secrets.get("OPENAI_API_KEY")
            except FileNotFoundError:
                self.api_key = None
        
        self.model = model
        self.client = None
        
        if self.api_key:
            if self.api_key.startswith("hf_"):
                self.client = openai.OpenAI(base_url="https://router.huggingface.co/hf-inference/v1/", api_key=self.api_key)
            elif self.api_key.startswith("AIza"):
                self.client = openai.OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=self.api_key)
            elif self.api_key.startswith("nvapi-"):
                self.client = openai.OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=self.api_key)
            else:
                self.client = openai.OpenAI(api_key=self.api_key)

    def generate_response(self, user_input, chat_history, profile, context_text=None, vision_bytes=None):
        """Generates a personalized tutor response based on history, profile, and optional vision images."""
        if not self.client:
            return "⚠️ LLM API Key not found. Please provide an API key in the environment variables."

        system_prompt = TUTOR_SYSTEM_PROMPT.format(
            skill_level=profile.get("skill_level", "Beginner"),
            teaching_mode=profile.get("teaching_mode", "Explain simply"),
            weak_topics=", ".join(profile.get("weak_topics", [])) or "None identified yet",
            context_section=f"\n\n### Document Context:\nUse the following extracted notes strictly to answer the user accurately:\n{context_text[:100000]}" if context_text else ""
        )

        messages = [{"role": "system", "content": system_prompt}]
        for msg in chat_history[-10:]:
            # Discard any large image payloads when bouncing to LLM context limits to save tokens
            if "image_data" not in msg:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        target_model = self.model
        
        # If user uploaded an image for Vision AI analysis
        if vision_bytes:
            import base64
            b64_img = base64.b64encode(vision_bytes).decode('utf-8')
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]
            })
            # Force target to NVIDIA's hosted vision model
            target_model = "meta/llama-3.2-90b-vision-instruct"
        else:
            messages.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"

    def generate_image(self, prompt_text):
        """Calls NVIDIA API for Stability SD3 image generation."""
        if not self.api_key or not self.api_key.startswith("nvapi-"):
            return "❌ Image generation is currently only configured for NVIDIA API keys."
            
        url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        payload = {
            "prompt": prompt_text,
            "seed": 0,
            "steps": 40
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if "image" in data:
                return data["image"]
            return f"❌ Unexpected API response format: {data}"
        except Exception as e:
            return f"❌ Image generation failed. Ensure your NVIDIA tokens are active. Err: {str(e)}"

    def analyze_weakness(self, chat_history):
        pass
