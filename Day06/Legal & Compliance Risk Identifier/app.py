import streamlit as st
import os
from dotenv import load_dotenv
import json
from pathlib import Path
from agents.startup_classifier import StartupClassifier
from agents.legal_risk import LegalRiskAgent
from agents.checklist_generator import ChecklistGenerator

# Load environment variables
load_dotenv()

# Initialize agents
@st.cache_resource
def initialize_agents():
    return {
        'classifier': StartupClassifier(),
        'risk_assessor': LegalRiskAgent(),
        'checklist_gen': ChecklistGenerator()
    }

agents = initialize_agents()

# Set page config
st.set_page_config(
    page_title="Legal & Compliance Risk Identifier",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        height: 150px;
    }
    .risk-alert {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .high-risk {
        background-color: #ffebee;
        border: 1px solid #ffcdd2;
    }
    .medium-risk {
        background-color: #fff3e0;
        border: 1px solid #ffe0b2;
    }
    .low-risk {
        background-color: #e8f5e9;
        border: 1px solid #c8e6c9;
    }
    .checklist-item {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("⚖️ Legal & Compliance Risk Identifier")
st.markdown("""
    This tool helps early-stage startups identify potential legal risks and compliance requirements 
    based on their business model and target markets.
""")

# Create sidebar for additional options
with st.sidebar:
    st.header("Settings")
    target_markets = st.multiselect(
        "Select Target Markets",
        ["United States", "European Union", "India", "United Kingdom", "Singapore"],
        default=["United States"]
    )
    
    st.header("About")
    st.info("""
        This tool uses AI to analyze your startup idea and provide:
        - Business model classification
        - Legal risk assessment
        - Compliance checklist
        - Relevant legal resources
    """)

# Main input area
st.header("Describe Your Startup")
startup_description = st.text_area(
    "Enter your startup idea in detail",
    placeholder="Example: We are building an AI-powered platform for remote medical consultations and storing user health records..."
)

# Optional file upload
uploaded_file = st.file_uploader(
    "Upload additional documents (optional)",
    type=["pdf", "docx", "txt"],
    help="Upload business plans, pitch decks, or other relevant documents"
)

# Submit button
if st.button("Analyze Legal Risks", type="primary"):
    if not startup_description:
        st.error("Please enter your startup description")
    else:
        with st.spinner("Analyzing your startup..."):
            # Step 1: Classify the startup
            classification = agents['classifier'].classify(startup_description)
            
            # Step 2: Assess legal risks
            risk_assessment = agents['risk_assessor'].assess_risks(
                startup_type=classification.business_model,
                target_markets=target_markets,
                startup_description=startup_description
            )
            
            # Step 3: Generate checklist
            checklist = agents['checklist_gen'].generate_checklist(
                startup_type=classification.business_model,
                target_markets=target_markets,
                risks=[risk.dict() for risk in risk_assessment.risks]
            )
            
            # Display results in tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "Business Classification", 
                "Legal Risks", 
                "Compliance Checklist",
                "Resources"
            ])
            
            with tab1:
                st.subheader("Business Classification")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Business Model", classification.business_model)
                    st.metric("Industry Vertical", classification.vertical)
                with col2:
                    st.metric("Sub-Vertical", classification.sub_vertical)
                    st.metric("Confidence Score", f"{classification.confidence_score:.2%}")
                
                st.subheader("Key Indicators")
                for keyword in classification.keywords:
                    st.markdown(f"- {keyword}")
            
            with tab2:
                st.subheader("Legal Risks Assessment")
                for risk in risk_assessment.risks:
                    risk_class = {
                        "High": "high-risk",
                        "Medium": "medium-risk",
                        "Low": "low-risk"
                    }.get(risk.risk_level, "medium-risk")
                    
                    st.markdown(f"""
                        <div class="risk-alert {risk_class}">
                            <h4>{risk.risk_category} ({risk.risk_level} Risk)</h4>
                            <p>{risk.description}</p>
                            <h5>Applicable Regulations:</h5>
                            <ul>
                                {''.join(f'<li>{reg}</li>' for reg in risk.applicable_regulations)}
                            </ul>
                            <h5>Mitigation Steps:</h5>
                            <ul>
                                {''.join(f'<li>{step}</li>' for step in risk.mitigation_steps)}
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.subheader("Priority Actions")
                for action in risk_assessment.priority_actions:
                    st.markdown(f"- {action}")
            
            with tab3:
                st.subheader("Compliance Checklist")
                st.metric("Total Estimated Cost", checklist.total_estimated_cost)
                st.metric("Recommended Timeline", checklist.timeline)
                
                for item in checklist.items:
                    st.markdown(f"""
                        <div class="checklist-item">
                            <h4>{item.category} - {item.priority} Priority</h4>
                            <p><strong>Task:</strong> {item.task}</p>
                            <p><strong>Deadline:</strong> {item.deadline}</p>
                            <p><strong>Estimated Cost:</strong> {item.estimated_cost}</p>
                            <p><strong>Resources:</strong></p>
                            <ul>
                                {''.join(f'<li>{resource}</li>' for resource in item.resources)}
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
            
            with tab4:
                st.subheader("Legal Resources")
                for market in target_markets:
                    st.markdown(f"### {market} Resources")
                    regulations = agents['risk_assessor'].get_common_regulations().get(market, [])
                    for reg in regulations:
                        st.markdown(f"- {reg}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ for startups | Not legal advice</p>
    </div>
""", unsafe_allow_html=True) 