from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict
import os
import csv

class LegalRisk(BaseModel):
    risk_level: str = Field(description="Level of risk (High, Medium, Low)")
    risk_category: str = Field(description="Category of legal risk (e.g., Data Privacy, IP, Compliance)")
    description: str = Field(description="Detailed description of the risk")
    applicable_regulations: List[str] = Field(description="List of applicable regulations or laws")
    mitigation_steps: List[str] = Field(description="Recommended steps to mitigate the risk")

class LegalRiskAssessment(BaseModel):
    startup_type: str = Field(description="The classified type of startup")
    target_markets: List[str] = Field(description="List of target markets/jurisdictions")
    risks: List[LegalRisk] = Field(description="List of identified legal risks")
    priority_actions: List[str] = Field(description="List of priority actions to address risks")

class LegalRiskAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=float(os.getenv("RISK_ASSESSOR_TEMPERATURE", "0.1")),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            convert_system_message_to_human=True
        )
        self.parser = PydanticOutputParser(pydantic_object=LegalRiskAssessment)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert legal risk assessor for startups.
            Your task is to identify potential legal risks and compliance requirements
            based on the startup's business model and target markets.
            Focus on data privacy, intellectual property, and regulatory compliance risks.
            Provide specific, actionable insights."""),
            ("user", """Analyze this startup for legal risks:
            Startup Type: {startup_type}
            Target Markets: {target_markets}
            Description: {startup_description}
            
            {format_instructions}""")
        ])

        self.domain_geo_risk_ruleset = {
            ("fintech", "EU"): [
                {"risk": "GDPR Non-compliance", "description": "Failure to protect personal data may result in heavy penalties under EU data protection law.", "jurisdiction": "EU"},
                {"risk": "PSD2 Licensing", "description": "Operating as a payment service provider in the EU requires PSD2 authorization.", "jurisdiction": "EU"},
                {"risk": "KYC/AML Requirements", "description": "Know Your Customer and Anti-Money Laundering regulations must be followed.", "jurisdiction": "EU"}
            ],
            ("healthtech", "US"): [
                {"risk": "HIPAA Non-compliance", "description": "Failure to protect health data may result in penalties under HIPAA.", "jurisdiction": "US"},
                {"risk": "FDA Approval", "description": "Medical devices/software may require FDA approval.", "jurisdiction": "US"}
            ]
        }

    def normalize_inputs(self, domain, geography):
        # Example normalization logic
        domain = domain.lower().strip()
        geography = geography.upper().strip()
        if geography in ["GERMANY", "FRANCE", "UNITED KINGDOM"]:
            geography = "EU"
        if domain in ["digital lending", "payments"]:
            domain = "fintech"
        return domain, geography

    def get_ruleset_risks(self, domain, geography):
        domain, geography = self.normalize_inputs(domain, geography)
        return self.domain_geo_risk_ruleset.get((domain, geography), [])

    def assess_risks(self, startup_type: str, target_markets: List[str], startup_description: str) -> LegalRiskAssessment:
        # Preprocessing: normalize and map risks
        risks = []
        for market in target_markets:
            mapped_risks = self.get_ruleset_risks(startup_type, market)
            risks.extend(mapped_risks)
        # Optionally, pass mapped risks to the LLM for further refinement
        try:
            formatted_prompt = self.prompt.format_messages(
                startup_type=startup_type,
                target_markets=", ".join(target_markets),
                startup_description=startup_description + f"\nKnown Risks: {risks}",
                format_instructions=self.parser.get_format_instructions()
            )
            response = self.llm.invoke(formatted_prompt)
            assessment = self.parser.parse(response.content)
            return assessment
        except Exception as e:
            print(f"Error in risk assessment: {str(e)}")
            return None

    def get_common_regulations(self) -> Dict[str, List[str]]:
        """Return a dictionary of common regulations by region."""
        return {
            "United States": [
                "HIPAA (Health Insurance Portability and Accountability Act)",
                "CCPA (California Consumer Privacy Act)",
                "GLBA (Gramm-Leach-Bliley Act)",
                "COPPA (Children's Online Privacy Protection Act)",
                "DMCA (Digital Millennium Copyright Act)"
            ],
            "European Union": [
                "GDPR (General Data Protection Regulation)",
                "ePrivacy Directive",
                "PSD2 (Payment Services Directive)",
                "Medical Device Regulation (MDR)"
            ],
            "India": [
                "Information Technology Act, 2000",
                "Personal Data Protection Bill",
                "RBI Guidelines for Fintech",
                "Telecom Commercial Communications Customer Preference Regulations"
            ]
        } 