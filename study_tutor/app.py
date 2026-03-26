import streamlit as st
import os
import base64
from dotenv import load_dotenv

load_dotenv()

from memory import MemoryManager
from tutor import PersonalTutor
from utils import sidebar_menu, styling, extract_text_from_file

# Page Config
st.set_page_config(page_title="StudyTutor AI", layout="wide", page_icon="🎓")

def main():
    styling()
    
    # Initialize components
    memory = MemoryManager()
    profile = memory.get_user_profile()
    
    # Sidebar UI
    _, profile = sidebar_menu(memory)
    
    # Study Guide Exporter
    st.sidebar.divider()
    st.sidebar.subheader("🗂️ Export Research")
    if st.sidebar.button("📝 Generate Study Guide"):
        chat_transcript = "\n".join([f"**{msg['role'].capitalize()}**: {msg['content']}" for msg in memory.get_chat_history() if "image_data" not in msg])
        
        # Pull latest context array directly from state memory 
        temp_context = st.session_state.get("current_context", "")
        if not chat_transcript.strip() and not temp_context:
            st.sidebar.warning("Add some chat history or upload a file first!")
        else:
            with st.sidebar.status("Synthesizing your Session...", expanded=True) as status:
                sys_msg = "You are an expert academic tutor. Summarize the following research context and conversations into a flawlessly structured Markdown Study Guide. Include heavily structured headings, concise bullet points, and key takeaways."
                payload = chat_transcript
                if temp_context:
                    payload += f"\n\nSource Material Used:\n{temp_context[:50000]}"
                
                try:
                    # Initialize Tutor
                    model_id = profile.get("model_id", "meta/llama3-70b-instruct")
                    temp_tutor = PersonalTutor(model=model_id)
                    res = temp_tutor.client.chat.completions.create(
                        model=temp_tutor.model, 
                        messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": f"Please synthesize this into a master study guide:\n\n{payload}"}],
                        temperature=0.5
                    )
                    st.session_state["study_guide"] = res.choices[0].message.content
                    status.update(label="Study Guide complete!", state="complete", expanded=False)
                except Exception as e:
                    status.update(label="Error generating guide.", state="error")
                    st.sidebar.error(str(e))

    if "study_guide" in st.session_state:
        st.sidebar.download_button("📥 Download as .md file", data=st.session_state["study_guide"], file_name="master_study_guide.md", mime="text/markdown")
        st.sidebar.caption("💡 **Tip:** To create a beautiful PDF, open this downloaded Markdown file in your browser, Github, or Notion, and simply press **Cmd+P** (Print to PDF)!")
        with st.sidebar.expander("Preview Study Guide"):
            st.markdown(st.session_state["study_guide"])

    # Initialize Tutor
    model_id = profile.get("model_id", "meta/llama3-70b-instruct")
    tutor = PersonalTutor(model=model_id)
    
    st.title("🎓 Personal Study Tutor")
    st.subheader("Interactive Learning Session")
    
    # Display chat history
    chat_history = memory.get_chat_history()
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image_data" in message:
                st.image(base64.b64decode(message["image_data"]))
                
    st.write("") # Spacing
    
    # Mode Selection UI
    action_mode = st.radio(
        "Select your action:", 
        options=["💬 Ask Tutor", "🎨 Generate Image"], 
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Document Upload UI (Bottom Area next to text-bar)
    with st.expander("📎 Attach Documents & Images for Analysis"):
        uploaded_files = st.file_uploader(
            "Upload files for the AI Tutor to read or see.", 
            type=["txt", "pdf", "png", "jpg", "jpeg"], 
            accept_multiple_files=True
        )
        
        context_text = ""
        vision_bytes = None
        
        if uploaded_files:
            docs = [f for f in uploaded_files if f.name.endswith(('.txt', '.pdf'))]
            imgs = [f for f in uploaded_files if f.name.endswith(('.png', '.jpg', '.jpeg'))]
            
            # Parse Docs
            for d in docs:
                ext = extract_text_from_file(d)
                if ext:
                    context_text += f"\n\n--- Document: {d.name} ---\n{ext}"
            
            # Save to session_state for Study Guide exporter mapping
            st.session_state["current_context"] = context_text
            
            # Interactive dropdown to 'see' the uploaded document text perfectly
            if context_text:
                with st.expander("👀 Verify Uploaded Document Text (Dropdown)"):
                    st.text_area("Extracted Content:", context_text, height=150)
            
            # Parse Images
            if imgs:
                vision_bytes = imgs[0].getvalue() # takes the first uploaded image
                st.image(vision_bytes, caption=f"Attached Image: {imgs[0].name}", width=150)
    
    # Prevent unbound local variable error if not uploaded
    if 'context_text' not in locals():
        context_text = ""
    if 'vision_bytes' not in locals():
        vision_bytes = None
        
    # Chat Input
    if prompt := st.chat_input(f"Type here to {'ask a question' if action_mode == '💬 Ask Tutor' else 'generate an image'}..."):
        
        # Add user message to UI and history
        with st.chat_message("user"):
            st.markdown(prompt)
            if action_mode == "🎨 Generate Image":
                st.caption("*(Requested Image Generation)*")
                
        # Format the user prompt history clearly so the LLM doesn't get confused by random image generation requests
        history_prompt = prompt if action_mode == "💬 Ask Tutor" else f"[User generated an image of: {prompt}]"
        memory.add_chat_message("user", history_prompt)
        
        # Image Generation Hook
        if action_mode == "🎨 Generate Image":
            with st.chat_message("assistant"):
                with st.spinner(f"Generating visual aid for '{prompt}'..."):
                    img_data = tutor.generate_image(prompt)
                    if img_data and not img_data.startswith("❌"):
                        st.image(base64.b64decode(img_data), caption=prompt)
                        
                        # Save the image string securely in the last JSON history array node
                        chat_history = memory.get_chat_history()
                        chat_history.append({
                            "role": "assistant", 
                            "content": f"**Generated Visual Aid:**", 
                            "image_data": img_data
                        })
                        memory.update_user_profile({"chat_history": chat_history})
                    else:
                        st.error(img_data)
                        memory.add_chat_message("assistant", img_data)
        else:
            # Generate and display tutor response for normal chat (or vision)
            with st.chat_message("assistant"):
                with st.spinner("Tutor is thinking/analyzing..."):
                    response = tutor.generate_response(prompt, chat_history, profile, context_text, vision_bytes=vision_bytes)
                    st.markdown(response)
                    memory.add_chat_message("assistant", response)
                    
    st.write("")
    if st.button("🗑️ Clear Chat History", key="clear_chat"):
        memory.clear_chat_history()
        st.rerun()

if __name__ == "__main__":
    main()
