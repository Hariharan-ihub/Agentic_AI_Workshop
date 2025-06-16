from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import os

class StartupClassification(BaseModel):
    business_model: str = Field(description="The primary business model of the startup")
    vertical: str = Field(description="The industry vertical (e.g., Fintech, Healthtech, Edtech)")
    sub_vertical: str = Field(description="More specific sub-category within the vertical")
    confidence_score: float = Field(description="Confidence score of the classification (0-1)")
    keywords: List[str] = Field(description="Key terms that indicate the business model")

class StartupClassifier:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=float(os.getenv("CLASSIFIER_TEMPERATURE", "0.1")),
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.parser = PydanticOutputParser(pydantic_object=StartupClassification)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert startup business model classifier. 
            Your task is to analyze startup descriptions and classify them into appropriate business models and verticals.
            Focus on identifying the primary business model and industry vertical.
            Be specific and accurate in your classification."""),
            ("user", """Analyze this startup description and classify it:
            {startup_description}
            
            {format_instructions}""")
        ])

    def classify(self, startup_description: str) -> StartupClassification:
        """Classify a startup based on its description."""
        try:
            # Format the prompt with the startup description
            formatted_prompt = self.prompt.format_messages(
                startup_description=startup_description,
                format_instructions=self.parser.get_format_instructions()
            )
            
            # Get the response from the LLM
            response = self.llm.invoke(formatted_prompt)
            
            # Parse the response into our Pydantic model
            classification = self.parser.parse(response.content)
            
            return classification
            
        except Exception as e:
            print(f"Error in classification: {str(e)}")
            return None

    def get_common_verticals(self) -> List[str]:
        """Return a list of common startup verticals for reference."""
        return [
            "Fintech",
            "Healthtech",
            "Edtech",
            "SaaS",
            "E-commerce",
            "AI/ML",
            "IoT",
            "Blockchain",
            "Cybersecurity",
            "CleanTech",
            "PropTech",
            "HRTech",
            "LegalTech",
            "AgriTech",
            "RetailTech"
        ] 