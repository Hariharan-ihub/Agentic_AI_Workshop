
import streamlit as st
import time
import google.generativeai as genai
import os
from typing import List, Tuple
import json

# Configure Gemini API
# For security, consider using environment variables
api_key = "AIzaSyDG-0xIaprzdT70VTf-LnMt62_s-F8SJqA"
genai.configure(api_key=api_key)

# System messages
CREATOR_SYSTEM_MESSAGE = """
You are a Content Creator Agent specializing in Generative AI. Your role is to:
1. Draft clear, concise, and technically accurate content
2. Revise content based on constructive feedback
3. Structure output in markdown format
4. Focus exclusively on content creation (no commentary)
5. Provide comprehensive coverage of the topic
"""

CRITIC_SYSTEM_MESSAGE = """
You are a Content Critic Agent evaluating Generative AI content. Your role is to:
1. Analyze technical accuracy and language clarity
2. Provide specific, constructive feedback
3. Identify both strengths and areas for improvement
4. Maintain professional, objective tone
5. Suggest concrete improvements
"""

# Agent class for content generation using direct Gemini API
class ContentAgent:
    def __init__(self, model_name: str, system_message: str):
        self.model_name = model_name
        self.system_message = system_message
        self.model = genai.GenerativeModel(model_name)
    
    def generate(self, prompt: str) -> str:
        """Generate content using the Gemini model"""
        full_prompt = f"{self.system_message}\n\n{prompt}"
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                    top_p=0.8,
                    top_k=40
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"

# Initialize agents
@st.cache_resource
def initialize_agents():
    creator = ContentAgent("gemini-1.5-flash", CREATOR_SYSTEM_MESSAGE)
    critic = ContentAgent("gemini-1.5-flash", CRITIC_SYSTEM_MESSAGE)
    return creator, critic

# Streamlit UI
st.set_page_config(
    page_title="Agentic AI Content Refinement",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic AI Content Refinement")
st.caption("Simulated conversation between Content Creator and Content Critic agents using Gemini AI")

# Sidebar controls
with st.sidebar:
    st.header("Configuration")
    topic = st.text_input("Discussion Topic", "Agentic AI", help="Enter the topic you want to create content about")
    turns = st.slider("Conversation Turns", min_value=3, max_value=7, value=3, step=2, 
                     help="Number of back-and-forth exchanges between agents")
    
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("1. **Creator** drafts initial content")
    st.markdown("2. **Critic** provides feedback")
    st.markdown("3. **Creator** revises based on feedback")
    st.markdown("4. Process continues for selected turns")

# Main content area
col1, col2 = st.columns([3, 1])

with col2:
    generate_btn = st.button("🚀 Start Simulation", type="primary", use_container_width=True)
    
    if st.button("Clear Results", use_container_width=True):
        if 'conversation_history' in st.session_state:
            del st.session_state['conversation_history']
        if 'final_content' in st.session_state:
            del st.session_state['final_content']
        st.rerun()

with col1:
    if generate_btn:
        # Initialize agents
        creator_agent, critic_agent = initialize_agents()
        
        # Initialize conversation state
        conversation_history: List[Tuple[str, str, str]] = []
        creator_output = ""
        critic_feedback = ""
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Start conversation
        for turn in range(1, turns + 1):
            progress = turn / turns
            progress_bar.progress(progress)
            
            with st.container():
                # Content Creator Turn (odd turns)
                if turn % 2 == 1:
                    status_text.text(f"🎨 Turn {turn}: Content Creator working...")
                    
                    if turn == 1:
                        prompt = f"""Draft comprehensive content about {topic} in markdown format covering:
- Key concepts and definitions
- Technical foundations
- Real-world applications and use cases
- Current challenges and limitations
- Future implications and trends

Make it informative, well-structured, and engaging."""
                    else:
                        prompt = f"""Revise this content based on the critic's feedback:

**Critic's Feedback:**
{critic_feedback}

**Current Content:**
{creator_output}

Provide improved markdown content that addresses the feedback while maintaining quality and structure."""
                    
                    # Generate content
                    with st.spinner("Content Creator is working..."):
                        creator_output = creator_agent.generate(prompt)
                    
                    conversation_history.append(("Creator", prompt, creator_output))
                
                # Content Critic Turn (even turns)
                else:
                    status_text.text(f"🔍 Turn {turn}: Content Critic analyzing...")
                    
                    prompt = f"""Evaluate this content on the following criteria:

1. **Technical Accuracy**: Are the concepts and information correct?
2. **Clarity of Explanations**: Are complex ideas explained clearly?
3. **Depth of Coverage**: Is the topic covered comprehensively?
4. **Structure and Organization**: Is the content well-organized?
5. **Engagement**: Is the content interesting and engaging?

**Content to Evaluate:**
{creator_output}

Provide specific, constructive feedback with concrete suggestions for improvement."""
                    
                    # Generate feedback
                    with st.spinner("Content Critic is analyzing..."):
                        critic_feedback = critic_agent.generate(prompt)
                    
                    conversation_history.append(("Critic", prompt, critic_feedback))
                
                time.sleep(0.5)  # Avoid rate limiting
        
        # Store results in session state
        st.session_state['conversation_history'] = conversation_history
        st.session_state['final_content'] = creator_output
        
        progress_bar.progress(1.0)
        status_text.text("✅ Simulation completed!")
        
        # Auto-scroll to results
        st.rerun()

# Display results if available
if 'final_content' in st.session_state:
    st.markdown("---")
    
    # Final output
    st.subheader("✅ Final Refined Content")
    with st.container():
        st.markdown(st.session_state['final_content'])
    
    # Download button for final content
    st.download_button(
        label="📥 Download Final Content",
        data=st.session_state['final_content'],
        file_name=f"refined_content_{topic.replace(' ', '_')}.md",
        mime="text/markdown"
    )
    
    st.markdown("---")
    
    # Conversation history
    st.subheader("🗨️ Conversation History")
    
    if 'conversation_history' in st.session_state:
        for i, (role, prompt, response) in enumerate(st.session_state['conversation_history'], 1):
            with st.expander(f"{role} - Turn {i} {'🎨' if role == 'Creator' else '🔍'}"):
                st.markdown("**Prompt:**")
                st.text(prompt)
                st.markdown("**Response:**")
                if role == "Creator":
                    st.markdown(response)
                else:
                    st.write(response)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Powered by Google Gemini AI | Built with Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)
