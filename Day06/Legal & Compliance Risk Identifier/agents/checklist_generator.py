from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict
import os

class ChecklistItem(BaseModel):
    category: str = Field(description="Category of the checklist item (e.g., Data Privacy, IP, Compliance)")
    task: str = Field(description="The specific task or action item")
    priority: str = Field(description="Priority level (High, Medium, Low)")
    deadline: str = Field(description="Recommended timeline for completion")
    resources: List[str] = Field(description="Helpful resources or references")
    estimated_cost: str = Field(description="Estimated cost range for completion")

class LegalChecklist(BaseModel):
    startup_type: str = Field(description="The type of startup")
    target_markets: List[str] = Field(description="Target markets/jurisdictions")
    items: List[ChecklistItem] = Field(description="List of checklist items")
    total_estimated_cost: str = Field(description="Total estimated cost for all items")
    timeline: str = Field(description="Overall recommended timeline")

class ChecklistGenerator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=float(os.getenv("CHECKLIST_GENERATOR_TEMPERATURE", "0.1")),
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.parser = PydanticOutputParser(pydantic_object=LegalChecklist)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert legal checklist generator for startups.
            Your task is to create detailed, actionable checklists for legal compliance
            based on the startup's business model, target markets, and identified risks.
            Focus on practical, implementable steps with realistic timelines and cost estimates."""),
            ("user", """Generate a legal compliance checklist for this startup:
            Startup Type: {startup_type}
            Target Markets: {target_markets}
            Identified Risks: {risks}
            
            {format_instructions}""")
        ])

    def generate_checklist(self, startup_type: str, target_markets: List[str], risks: List[Dict]) -> LegalChecklist:
        """Generate a legal compliance checklist."""
        try:
            # Format the prompt with startup information
            formatted_prompt = self.prompt.format_messages(
                startup_type=startup_type,
                target_markets=", ".join(target_markets),
                risks=str(risks),
                format_instructions=self.parser.get_format_instructions()
            )
            
            # Get the response from the LLM
            response = self.llm.invoke(formatted_prompt)
            
            # Parse the response into our Pydantic model
            checklist = self.parser.parse(response.content)
            
            return checklist
            
        except Exception as e:
            print(f"Error in checklist generation: {str(e)}")
            return None

    def get_common_checklist_categories(self) -> List[str]:
        """Return a list of common checklist categories."""
        return [
            "Business Registration",
            "Data Privacy & Security",
            "Intellectual Property",
            "Terms & Conditions",
            "Employment & Labor",
            "Tax Compliance",
            "Industry-Specific Regulations",
            "Contract Management",
            "Insurance Requirements",
            "Export Controls"
        ] 