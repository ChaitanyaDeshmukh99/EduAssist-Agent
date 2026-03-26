import json
import os
import streamlit as st

class MemoryManager:
    def __init__(self, storage_path="data/user_data.json"):
        self.storage_path = storage_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
                json.dump({}, f)

    def load_user_data(self):
        """Loads persistent user data from JSON."""
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_user_data(self, data):
        """Saves persistent user data to JSON."""
        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=4)

    def get_user_profile(self):
        """Retrieves user profile from session state or persistent storage."""
        if "user_profile" not in st.session_state:
            persistent_data = self.load_user_data()
            st.session_state.user_profile = persistent_data.get("profile", {
                "subject": "General",
                "skill_level": "Beginner",
                "teaching_mode": "Explain simply",
                "weak_topics": [],
                "topics_studied": [],
                "quiz_history": []
            })
        return st.session_state.user_profile

    def update_user_profile(self, updates):
        """Updates user profile in session state and persistent storage."""
        profile = self.get_user_profile()
        profile.update(updates)
        st.session_state.user_profile = profile
        
        persistent_data = self.load_user_data()
        persistent_data["profile"] = profile
        self.save_user_data(persistent_data)

    def add_chat_message(self, role, content):
        """Adds a message to the short-term chat history."""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append({"role": role, "content": content})

    def get_chat_history(self):
        """Retrieves chat history from session state."""
        return st.session_state.get("chat_history", [])

    def clear_chat_history(self):
        """Clears chat history in session state."""
        st.session_state.chat_history = []
