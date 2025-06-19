from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict
import os

class ChecklistItem(BaseModel):
    task: str = Field(description="Checklist task")
    description: str = Field(description="Task description")
    responsible: str = Field(description="Responsible role")
    stage: str = Field(description="Due stage (e.g., Pre-launch, Post-launch)")

class LegalChecklist(BaseModel):
    sector: str = Field(description="The sector of the startup")
    geography: str = Field(description="Geographical region")
    risks: List[str] = Field(description="List of risks")
    items: List[ChecklistItem] = Field(description="List of checklist items")

class ChecklistGenerator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=float(os.getenv("CHECKLIST_GENERATOR_TEMPERATURE", "0.1")),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            convert_system_message_to_human=True
        )
        self.parser = PydanticOutputParser(pydantic_object=LegalChecklist)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a legal compliance expert.\nCreate a compliance checklist for a {sector} startup in {geography} with the following risks:\n{risks}\nFormat each checklist item with:\n- Task\n- Description\n- Responsible Role\n- Due Stage (e.g., Pre-launch, Post-launch)\n"""),
            ("user", """Checklist format:\n{format_instructions}""")
        ])

    def generate_checklist(self, sector: str, geography: str, risks: List[str]) -> LegalChecklist:
        try:
            formatted_prompt = self.prompt.format_messages(
                sector=sector,
                geography=geography,
                risks="\n".join(risks),
                format_instructions=self.parser.get_format_instructions()
            )
            response = self.llm.invoke(formatted_prompt)
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