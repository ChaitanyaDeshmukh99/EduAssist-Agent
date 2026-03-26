import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from memory import MemoryManager
from tutor import PersonalTutor
from quiz import QuizSystem
from utils import sidebar_menu, display_stats, styling

# Page Config
st.set_page_config(page_title="StudyTutor AI", layout="wide", page_icon="🎓")

def main():
    styling()
    
    # Initialize components
    memory = MemoryManager()
    profile = memory.get_user_profile()
    
    # Sidebar UI
    api_key, profile = sidebar_menu(memory)
    display_stats(profile)
    
    # Initialize Tutor and Quiz
    model_id = profile.get("model_id", "mistralai/Mistral-7B-Instruct-v0.2")
    tutor = PersonalTutor(api_key=api_key, model=model_id)
    quiz_system = QuizSystem(tutor)
    
    # Tabs for Chat and Quiz
    st.title(f"🎓 Personal Study Tutor: {profile.get('subject', 'General')}")
    tab_chat, tab_quiz = st.tabs(["💬 Chat & Learn", "📝 Practice Quiz"])
    
    # --- CHAT TAB ---
    with tab_chat:
        st.subheader("Interactive Learning Session")
        
        # Display chat history
        chat_history = memory.get_chat_history()
        for message in chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat Input
        if prompt := st.chat_input("Ask a question about the topic..."):
            # Add user message to UI and history
            with st.chat_message("user"):
                st.markdown(prompt)
            memory.add_chat_message("user", prompt)
            
            # Generate and display tutor response
            with st.chat_message("assistant"):
                with st.spinner("Tutor is thinking..."):
                    response = tutor.generate_response(prompt, chat_history, profile)
                    st.markdown(response)
                    memory.add_chat_message("assistant", response)
                    
            # Update topics studied if not already
            if profile["subject"] not in profile.get("topics_studied", []):
                profile["topics_studied"].append(profile["subject"])
                memory.update_user_profile({"topics_studied": profile["topics_studied"]})
        
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            memory.clear_chat_history()
            st.rerun()

    # --- QUIZ TAB ---
    with tab_quiz:
        st.subheader(f"Quiz on {profile.get('subject', 'General')}")
        
        if st.button("🎯 Generate New Quiz"):
            with st.spinner("Generating quiz questions..."):
                quiz_data = quiz_system.generate_quiz(profile["subject"], profile)
                if quiz_data:
                    st.session_state.current_quiz = quiz_data
                    st.session_state.answers_submitted = False
                    st.session_state.quiz_feedback = None
                    st.rerun()

        if "current_quiz" in st.session_state:
            quiz = st.session_state.current_quiz
            st.info(f"Topic: {quiz.get('quiz_title', profile['subject'])}")
            
            with st.form("quiz_form"):
                user_answers = {}
                for idx, q in enumerate(quiz.get("questions", [])):
                    st.markdown(f"**Q{idx+1}: {q['question']}**")
                    if q["type"] == "mcq":
                        user_answers[f"q{q['id']}"] = st.radio(f"Select an option for Q{idx+1}:", q["options"], key=f"ans_{q['id']}")
                    else:
                        user_answers[f"q{q['id']}"] = st.text_input(f"Your answer for Q{idx+1}:", key=f"ans_{q['id']}")
                    st.divider()

                submitted = st.form_submit_state = st.form_submit_button("Submit Answers")
                
                if submitted:
                    with st.spinner("Evaluating your answers..."):
                        feedback = quiz_system.evaluate_quiz(quiz, user_answers, profile)
                        st.session_state.quiz_feedback = feedback
                        st.session_state.answers_submitted = True
                        
                        # Update stats based on feedback (very simple logic here)
                        # We'll just assume score is parsed from feedback or just log history
                        history = profile.get("quiz_history", [])
                        history.append({"topic": profile["subject"], "timestamp": "now"}) 
                        memory.update_user_profile({"quiz_history": history})

            if st.session_state.get("answers_submitted"):
                st.subheader("Feedback & Explanations")
                st.markdown(st.session_state.quiz_feedback)

if __name__ == "__main__":
    main()
