from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import os
import spacy

class StartupClassification(BaseModel):
    business_model: str = Field(description="The primary business model of the startup")
    vertical: str = Field(description="The industry vertical (e.g., Fintech, Healthtech, Edtech)")
    sub_vertical: str = Field(description="More specific sub-category within the vertical")
    confidence_score: float = Field(description="Confidence score of the classification (0-1)")
    keywords: List[str] = Field(description="Key terms that indicate the business model")

class StartupClassifier:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=float(os.getenv("CLASSIFIER_TEMPERATURE", "0.1")),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            convert_system_message_to_human=True
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

        self.nlp = spacy.load("en_core_web_sm")
        self.city_to_country = {
            "Berlin": "Germany",
            "Paris": "France",
            "London": "United Kingdom",
            # Add more mappings as needed
        }
        self.country_to_region = {
            "Germany": "EU",
            "France": "EU",
            "United Kingdom": "EU",
            "United States": "US",
            # Add more mappings as needed
        }

    def extract_and_normalize(self, text: str):
        doc = self.nlp(text)
        geographies = set()
        domains = set()
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                city = ent.text
                country = self.city_to_country.get(city, city)
                region = self.country_to_region.get(country, country)
                geographies.add(region)
            if ent.label_ in ["ORG", "PRODUCT"]:
                domains.add(ent.text)
        return list(domains), list(geographies)

    def classify(self, startup_description: str) -> StartupClassification:
        """Classify a startup based on its description."""
        # Preprocessing: extract and normalize domain/geography
        domains, geographies = self.extract_and_normalize(startup_description)
        # Optionally, use these in the prompt or as additional context
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
            
            # Optionally, attach extracted domains/geographies to the result
            classification.keywords.extend(domains + geographies)
            
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