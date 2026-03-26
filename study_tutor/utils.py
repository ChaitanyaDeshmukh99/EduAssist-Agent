import streamlit as st

def sidebar_menu(memory):
    """Renders the sidebar for user preferences."""
    st.sidebar.title("🎓 Tutor Settings")
    
    profile = memory.get_user_profile()
    
    # Subject Selection
    subjects = ["Python", "Machine Learning", "Data Science", "DevOps", "Mathematics", "Custom"]
    current_subject = profile.get("subject", "Python")
    subject_index = subjects.index(current_subject) if current_subject in subjects else 0
    subject = st.sidebar.selectbox("Subject", subjects, index=subject_index)
    
    if subject == "Custom":
        subject = st.sidebar.text_input("Specify Subject", value=profile.get("subject", ""))
    
    # Skill Level Selection
    levels = ["Beginner", "Intermediate", "Advanced"]
    current_level = profile.get("skill_level", "Beginner")
    level_index = levels.index(current_level) if current_level in levels else 0
    level = st.sidebar.selectbox("Skill Level", levels, index=level_index)
    
    # Teaching Mode Selection
    modes = ["Explain simply", "Step-by-step", "Exam mode", "Real-world examples"]
    current_mode = profile.get("teaching_mode", "Explain simply")
    mode_index = modes.index(current_mode) if current_mode in modes else 0
    mode = st.sidebar.selectbox("Teaching Mode", modes, index=mode_index)
    
    st.sidebar.divider()
    st.sidebar.subheader("🤖 LLM Settings")
    
    # Model Selection
    available_models = {
        "Gemini 2.5 Flash (Google)": "gemini-2.5-flash",
        "Gemini 2.5 Pro (Google)": "gemini-2.5-pro",
        "Mistral 7B (HF)": "mistralai/Mistral-7B-Instruct-v0.2",
        "Gemma 7B (HF)": "google/gemma-7b-it",
        "GPT-4o (OpenAI)": "gpt-4o",
        "GPT-3.5 Turbo": "gpt-3.5-turbo"
    }
    current_model_id = profile.get("model_id", "mistralai/Mistral-7B-Instruct-v0.2")
    model_name = st.sidebar.selectbox("Select Model", list(available_models.keys()), 
                                    index=list(available_models.values()).index(current_model_id) if current_model_id in available_models.values() else 0)
    model_id = available_models[model_name]

    # Update profile if changed
    if (subject != profile["subject"] or 
        level != profile["skill_level"] or 
        mode != profile["teaching_mode"] or
        model_id != profile.get("model_id")):
        
        memory.update_user_profile({
            "subject": subject,
            "skill_level": level,
            "teaching_mode": mode,
            "model_id": model_id
        })
        st.sidebar.success("Settings Updated!")

    return None, profile

def display_stats(profile):
    """Displays user progress stats in the sidebar or a separate section."""
    st.sidebar.divider()
    st.sidebar.subheader("📊 Progress Summary")
    
    st.sidebar.write(f"**Topics Studied:** {len(profile.get('topics_studied', []))}")
    st.sidebar.write(f"**Weak Topics:** {', '.join(profile.get('weak_topics', [])) or 'None'}")
    
    history = profile.get("quiz_history", [])
    if history:
        avg_score = sum([q.get('score', 0) for q in history]) / len(history)
        st.sidebar.write(f"**Avg Quiz Accuracy:** {avg_score:.1f}/3")
    else:
        st.sidebar.write("**Avg Quiz Accuracy:** N/A")

def styling():
    """Injects custom CSS for a premium look."""
    st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #f9a8d4;
    }
    </style>
    """, unsafe_allow_html=True)
