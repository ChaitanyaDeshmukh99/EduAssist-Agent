import streamlit as st
import io
import PyPDF2

def extract_text_from_file(uploaded_file):
    if not uploaded_file:
        return None
    try:
        if uploaded_file.name.endswith(".txt"):
            return uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")
    return None

def sidebar_menu(memory):
    """Renders the sidebar for user preferences."""
    st.sidebar.title("🎓 Tutor Settings")
    
    profile = memory.get_user_profile()
    
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
    
    # Update profile if changed
    if (level != profile.get("skill_level") or 
        mode != profile.get("teaching_mode")):
        
        memory.update_user_profile({
            "skill_level": level,
            "teaching_mode": mode
        })
        st.sidebar.success("Settings Updated!")

    return None, profile

def styling():
    """Injects custom CSS for a premium look."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;700&display=swap');

    /* Global Typography */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: #E2E8F0 !important;
        letter-spacing: -0.5px;
    }
    
    /* Main Background Gradient App */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #171124 0%, #020617 60%, #000000 100%);
    }

    /* Hide Default Elements for native app feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* Premium Chat Messages */
    .stChatMessage {
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease-in-out;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* The Avatar icons */
    .stChatMessage [data-testid="stChatMessageAvatarUser"] {
        background-color: #ec4899;
    }
    .stChatMessage [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #6366f1;
    }

    /* Input Area */
    [data-testid="stChatInput"] {
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        background: rgba(15, 23, 42, 0.8) !important;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Sidebar Aesthetics */
    [data-testid="stSidebar"] {
        background-color: rgba(9, 9, 11, 0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
    }
    
    /* Title Gradients */
    h1 {
        background: -webkit-linear-gradient(45deg, #ec4899, #8b5cf6, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)
