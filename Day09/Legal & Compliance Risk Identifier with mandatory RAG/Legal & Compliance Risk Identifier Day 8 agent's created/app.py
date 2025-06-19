import streamlit as st
import os
from dotenv import load_dotenv
from agents import BusinessModelAnalyzer, RiskDetectionAgent, LegalRetrieverAgent, ChecklistGeneratorAgent
import json
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize Streamlit page
st.set_page_config(
    page_title="Legal & Compliance Risk Identifier",
    page_icon="⚖️",
    layout="wide"
)

# Initialize agents
business_analyzer = BusinessModelAnalyzer()
risk_detector = RiskDetectionAgent()
legal_retriever = LegalRetrieverAgent()
checklist_generator = ChecklistGeneratorAgent()

# Set up the Streamlit interface
st.title("Legal & Compliance Risk Identifier")
st.write("Enter your business description to analyze legal and compliance risks.")

# Business Description Input
st.subheader("📝 Business Description")
business_description = st.text_area(
    "Enter your business details",
    placeholder="Describe your business, including:\n- Industry/Domain\n- Geographic location\n- Target market\n- Key operations and services\n- Business model",
    height=150
)

if business_description:
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Analyze business model
        with st.spinner("Analyzing business model..."):
            business_analysis = business_analyzer.analyze(business_description)
            st.subheader("🏢 Business Analysis")
            st.markdown("""
            **Domain:** {domain}  
            **Geography:** {geography}  
            **Operations:** {operations}  
            **Target Market:** {target_market}
            """.format(
                domain=business_analysis['domain'],
                geography=business_analysis['geography'],
                operations=business_analysis.get('operations', 'Not specified'),
                target_market=business_analysis.get('target_market', 'Not specified')
            ))

        # Analyze legal risks
        with st.spinner("Analyzing legal and compliance risks..."):
            risk_profile = risk_detector.analyze_risks(
                business_analysis['domain'],
                business_analysis['geography']
            )
            
            st.subheader("⚠️ Legal Risk Analysis")
            st.markdown(f"**Risk Level:** {risk_profile.get('risk_level', 'Medium')}")
            st.markdown(f"**Total Risks Identified:** {risk_profile.get('total_risks', 0)}")
            
            st.markdown("**Key Risk Areas:**")
            for risk in risk_profile['risks']:
                with st.expander(f"🔍 {risk.get('risk_name', 'Unknown Risk')}"):
                    st.markdown(f"**Severity:** {risk.get('severity', 'Medium')}")
                    st.markdown(f"**Description:** {risk.get('description', 'No description available')}")
                    st.markdown(f"**Applicable Laws:** {risk.get('law_or_framework', 'No applicable laws specified')}")
                    st.markdown(f"**Status:** {risk.get('status', 'Pending')}")

    with col2:
        # Retrieve legal information
        with st.spinner("Retrieving legal information..."):
            legal_info = legal_retriever.retrieve_legal_info(
                business_analysis['domain'],
                business_analysis['geography']
            )
            st.subheader("📚 Legal Information")
            st.markdown(legal_info['summary'])
            
            st.markdown("**Legal Sources:**")
            for source in legal_info['sources']:
                with st.expander(f"📄 {source.get('source', 'Unknown Source')}"):
                    if 'summary' in source:
                        st.markdown("**Summary:**")
                        st.markdown(source['summary'])
                    if 'content' in source:
                        st.markdown("**Content Preview:**")
                        st.markdown(source['content'][:500] + "...")
                    if 'jurisdiction' in source:
                        st.markdown(f"**Jurisdiction:** {source['jurisdiction']}")
                    if 'type' in source:
                        st.markdown(f"**Document Type:** {source['type']}")

    # Generate and display compliance checklist
    with st.spinner("Generating compliance checklist..."):
        checklist = checklist_generator.generate_checklist(
            domain=business_analysis['domain'],
            geography=business_analysis['geography'],
            stage="Early-stage",  # This could be made dynamic based on business description
            risks=risk_profile['risks'],
            legal_docs=legal_info['sources']
        )
        
        st.subheader("📋 Compliance Checklist")
        st.markdown(checklist['checklist'])
        
        # Add download button for the checklist
        checklist_json = json.dumps(checklist, indent=2)
        st.download_button(
            label="Download Checklist",
            data=checklist_json,
            file_name="compliance_checklist.json",
            mime="application/json"
        )

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, LangChain, and Google's Generative AI") 