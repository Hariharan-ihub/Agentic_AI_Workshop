import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from pydantic import BaseModel, Field
from utils import search_vector_store, VectorStore
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

load_dotenv()

class BusinessDescription(BaseModel):
    """Schema for business description input"""
    business_description: str = Field(
        description="A detailed description of the business.",
        default=""
    )

    class Config:
        """Pydantic model configuration"""
        arbitrary_types_allowed = True

class Risk(BaseModel):
    """Schema for risk information"""
    risk_name: str = Field(description="Short label for the risk")
    law_or_framework: str = Field(description="Applicable law or framework")
    description: str = Field(description="Detailed explanation of the risk")
    severity: str = Field(description="Risk severity level (High/Medium/Low)")
    status: str = Field(description="Risk status (Pending/Reviewed)", default="Pending")

class RiskProfile(BaseModel):
    domain: str = Field(description="Business domain")
    geography: str = Field(description="Geographic region")
    risks: List[Risk] = Field(description="List of identified risks")
    source: str = Field(description="Source of the risk analysis")
    justification: str = Field(description="Justification for the identified risks")

class BusinessModelAnalyzer:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings,
            collection_name="business_analysis"
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a business model analyzer. Analyze the given business description and identify:
            1. Primary business domain (e.g., fintech, healthtech, e-commerce)
            2. Operational geography (countries/regions of operation)
            3. Target market
            4. Key business activities
            Return the analysis in a structured format."""),
            ("human", "{business_description}")
        ])

    def analyze(self, business_description: str) -> Dict[str, str]:
        chain = LLMChain(llm=self.llm, prompt=self.prompt)
        result = chain.run(business_description=business_description)
        
        # Store in vector DB
        self.vector_db.add_texts(
            texts=[business_description],
            metadatas=[{"type": "business_analysis", "result": result}]
        )
        
        return {"domain": result, "geography": result}

class RiskDetectionAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings,
            collection_name="risk_profiles"
        )
        
        # Initialize risk detection prompt
        self.risk_detection_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a legal risk detection expert. Analyze the startup context and identify potential legal and compliance risks. For each identified risk, provide the following information in a structured format: risk_name: Short label for the risk, law_or_framework: Applicable law or framework, description: Detailed explanation of the risk, severity: High/Medium/Low, status: Pending. Consider these key areas: 1. Data Privacy & Protection (GDPR, HIPAA, CCPA) 2. Intellectual Property (Patents, Trademarks, Copyrights) 3. Tax Compliance (Corporate, Sales, International) 4. Industry-Specific Regulations 5. Employment Laws 6. Contractual Obligations 7. International Trade & Export Controls 8. Environmental Regulations 9. Consumer Protection Laws 10. Financial Regulations. Format the output as a JSON array of risk objects."),
            ("human", "Analyze risks for: Domain: {domain}, Geography: {geography}, Stage: {stage}, Description: {description}")
        ])

    def _retrieve_similar_risks(self, domain: str, geography: str, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Retrieve similar risks from vector DB"""
        query = f"{domain} {geography} legal risks"
        results = self.vector_db.similarity_search_with_score(query, k=5)
        
        similar_risks = []
        for doc, score in results:
            if score >= threshold:
                try:
                    risk_data = json.loads(doc.page_content)
                    similar_risks.append(risk_data)
                except:
                    continue
        
        return similar_risks

    def _parse_llm_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response into structured risk objects"""
        try:
            # Try to parse as JSON
            risks = json.loads(response)
            if isinstance(risks, list):
                return risks
        except:
            # If JSON parsing fails, try to extract risks from text
            risks = []
            current_risk = {}
            
            for line in response.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if '"risk_name":' in line:
                    if current_risk:
                        risks.append(current_risk)
                    current_risk = {'risk_name': line.split('"risk_name":')[1].strip().strip('",')}
                elif '"law_or_framework":' in line:
                    current_risk['law_or_framework'] = line.split('"law_or_framework":')[1].strip().strip('",')
                elif '"description":' in line:
                    current_risk['description'] = line.split('"description":')[1].strip().strip('",')
                elif '"severity":' in line:
                    current_risk['severity'] = line.split('"severity":')[1].strip().strip('",')
                elif '"status":' in line:
                    current_risk['status'] = line.split('"status":')[1].strip().strip('",')
            
            if current_risk:
                risks.append(current_risk)
        
        return risks

    def analyze_risks(self, domain: str, geography: str, stage: str = "MVP", description: str = "") -> Dict[str, Any]:
        """Analyze risks based on startup context"""
        # 1. Try to retrieve similar risks from vector DB
        similar_risks = self._retrieve_similar_risks(domain, geography)
        
        # 2. If not enough similar risks found, use LLM
        if len(similar_risks) < 3:
            chain = LLMChain(llm=self.llm, prompt=self.risk_detection_prompt)
            response = chain.run(
                domain=domain,
                geography=geography,
                stage=stage,
                description=description
            )
            
            # Parse LLM response
            llm_risks = self._parse_llm_response(response)
            
            # Combine with similar risks
            all_risks = similar_risks + llm_risks
            
            # Remove duplicates based on risk_name
            seen_risks = set()
            unique_risks = []
            for risk in all_risks:
                if risk['risk_name'] not in seen_risks:
                    seen_risks.add(risk['risk_name'])
                    unique_risks.append(risk)
            
            risks = unique_risks
        else:
            risks = similar_risks
        
        # Store in vector DB
        for risk in risks:
            self.vector_db.add_texts(
                texts=[json.dumps(risk)],
                metadatas=[{
                    "type": "risk_profile",
                    "domain": domain,
                    "geography": geography,
                    "stage": stage
                }]
            )
        
        # Calculate overall risk level
        severity_scores = {'High': 3, 'Medium': 2, 'Low': 1}
        max_severity = max(
            [severity_scores.get(r.get('severity', 'Medium').lower().capitalize(), 2) for r in risks],
            default=2
        )
        risk_level = 'High' if max_severity == 3 else 'Medium' if max_severity == 2 else 'Low'
        
        return {
            "risks": risks,
            "risk_level": risk_level,
            "total_risks": len(risks),
            "risk_categories": list(set(r.get('law_or_framework', '').split(':')[0] for r in risks if r.get('law_or_framework', '')))
        }

class LegalRetrieverAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings,
            collection_name="legal_documents"
        )
        
        # Initialize Hugging Face model for legal text classification
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN")
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        # Legal API endpoints
        self.legal_apis = {
            "law_cornell": "https://www.law.cornell.edu/api/v1/search",
            "findlaw": "https://www.findlaw.com/api/v1/search",
            "justia": "https://www.justia.com/api/v1/search",
            "lexology": "https://www.lexology.com/api/v1/search",
            "law360": "https://www.law360.com/api/v1/search"
        }
        
        # Government API endpoints
        self.gov_apis = {
            "us_gov": "https://api.regulations.gov/v4/documents",
            "eu_gov": "https://eur-lex.europa.eu/api/v1/search",
            "uk_gov": "https://www.legislation.gov.uk/api/v1/search"
        }
        
        # Initialize prompts
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a legal information expert. Analyze and summarize the legal information retrieved from various sources.
            Focus on:
            1. Applicable laws and regulations
            2. Compliance requirements
            3. Best practices
            4. Recent updates or changes
            Provide a clear, actionable summary."""),
            ("human", "Query: {query}\nContext: {context}")
        ])

    def _scrape_legal_website(self, url: str, headers: Dict[str, str] = None) -> str:
        """Scrape content from legal websites"""
        try:
            response = requests.get(url, headers=headers or {'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'footer']):
                element.decompose()
            
            # Extract main content
            content = soup.get_text(separator='\n', strip=True)
            return content
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return ""

    def _query_huggingface_model(self, text: str, task: str = "legal-classification") -> Dict[str, Any]:
        """Query Hugging Face model for legal text analysis"""
        try:
            API_URL = f"https://api-inference.huggingface.co/models/legal-bert-base-uncased"
            response = requests.post(API_URL, headers=self.headers, json={"inputs": text})
            return response.json()
        except Exception as e:
            print(f"Error querying Hugging Face model: {str(e)}")
            return {}

    def _fetch_legal_api_data(self, api_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch data from legal APIs"""
        try:
            response = requests.get(api_url, params=params)
            return response.json()
        except Exception as e:
            print(f"Error fetching from {api_url}: {str(e)}")
            return {}

    def _fetch_gov_regulations(self, jurisdiction: str, query: str) -> List[Dict[str, Any]]:
        """Fetch regulations from government APIs"""
        regulations = []
        
        if jurisdiction.lower() in ['us', 'united states']:
            api_url = self.gov_apis['us_gov']
            params = {
                'api_key': os.getenv('REGULATIONS_GOV_API_KEY'),
                'q': query,
                'sort': 'relevance'
            }
            data = self._fetch_legal_api_data(api_url, params)
            if data and 'data' in data:
                regulations.extend(data['data'])
        
        elif jurisdiction.lower() in ['eu', 'european union']:
            api_url = self.gov_apis['eu_gov']
            params = {
                'q': query,
                'type': 'regulation'
            }
            data = self._fetch_legal_api_data(api_url, params)
            if data and 'results' in data:
                regulations.extend(data['results'])
        
        return regulations

    def retrieve_legal_info(self, query: str, jurisdiction: str) -> Dict[str, Any]:
        """Retrieve legal information using multiple sources"""
        legal_info = []
        
        # 1. Scrape legal websites
        for source_name, api_url in self.legal_apis.items():
            content = self._scrape_legal_website(f"{api_url}?q={query}%20{jurisdiction}")
            if content:
                legal_info.append({
                    "source": source_name,
                    "content": content[:1000],  # Limit content length
                    "type": "web_scrape"
                })
        
        # 2. Fetch government regulations
        regulations = self._fetch_gov_regulations(jurisdiction, query)
        for reg in regulations:
            legal_info.append({
                "source": "government_api",
                "content": reg.get('description', ''),
                "type": "regulation",
                "jurisdiction": jurisdiction
            })
        
        # 3. Analyze content with Hugging Face model
        for info in legal_info:
            if info['content']:
                analysis = self._query_huggingface_model(info['content'])
                if analysis:
                    info['analysis'] = analysis
        
        # Store in vector DB
        texts = []
        metadatas = []
        
        for info in legal_info:
            if info['content'] and isinstance(info['content'], str):
                texts.append(info['content'])
                metadata = {
                    "type": "legal_info",
                    "source": info['source'],
                    "query": query,
                    "jurisdiction": jurisdiction
                }
                if 'analysis' in info:
                    metadata['analysis'] = str(info['analysis'])  # Convert analysis to string
                metadatas.append(metadata)
        
        if texts:  # Only add to vector DB if we have texts
            try:
                self.vector_db.add_texts(
                    texts=texts,
                    metadatas=metadatas
                )
            except Exception as e:
                print(f"Error adding to vector DB: {str(e)}")
        
        # Generate summary using LLM
        context = "\n".join([info['content'] for info in legal_info if info['content']])
        chain = LLMChain(llm=self.llm, prompt=self.prompt)
        summary = chain.run(query=query, context=context)
        
        return {
            "summary": summary,
            "sources": legal_info,
            "jurisdiction": jurisdiction,
            "query": query
        }

class ChecklistGeneratorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings,
            collection_name="compliance_checklists"
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a compliance checklist generator expert. Create a comprehensive compliance checklist based on:
            1. Business domain and geography
            2. Identified legal risks
            3. Retrieved legal documents and regulations
            
            Organize the checklist into clear categories:
            - Data Privacy & Protection
            - Intellectual Property
            - Tax & Financial Compliance
            - Corporate & Operational
            - Employment & Labor
            - Sector-Specific Regulations
            
            For each item, provide:
            - Clear action item
            - Applicable regulation/law
            - Priority level
            - Implementation timeline
            - Required documentation
            
            Format the output in a structured, easy-to-follow checklist format."""),
            ("human", """Business Info:
            Domain: {domain}
            Geography: {geography}
            Stage: {stage}
            
            Identified Risks:
            {risks}
            
            Legal Documents:
            {legal_docs}""")
        ])

    def generate_checklist(self, 
                         domain: str, 
                         geography: str, 
                         stage: str,
                         risks: List[Dict[str, Any]],
                         legal_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a compliance checklist based on business information, risks, and legal documents.
        
        Args:
            domain: Business domain/sector
            geography: Geographic region of operation
            stage: Business stage (e.g., early-stage, growth)
            risks: List of identified risks from RiskDetectionAgent
            legal_docs: List of legal documents from LegalRetrieverAgent
            
        Returns:
            Dict containing the generated checklist and metadata
        """
        # Format risks and legal docs for prompt
        risks_text = "\n".join([
            f"- {risk.get('risk_name', 'Unknown')}: {risk.get('description', 'No description')} "
            f"(Severity: {risk.get('severity', 'Medium')})"
            for risk in risks
        ])
        
        legal_docs_text = "\n".join([
            f"- {doc.get('summary', 'No summary available')}"
            for doc in legal_docs
        ])
        
        # Generate checklist using LLM
        chain = LLMChain(llm=self.llm, prompt=self.prompt)
        checklist = chain.run(
            domain=domain,
            geography=geography,
            stage=stage,
            risks=risks_text,
            legal_docs=legal_docs_text
        )
        
        # Store in vector DB
        self.vector_db.add_texts(
            texts=[checklist],
            metadatas=[{
                "type": "compliance_checklist",
                "domain": domain,
                "geography": geography,
                "stage": stage
            }]
        )
        
        return {
            "checklist": checklist,
            "metadata": {
                "domain": domain,
                "geography": geography,
                "stage": stage,
                "generated_at": str(datetime.now())
            }
        }

class ComplianceWorkflow:
    def __init__(self):
        self.business_analyzer = BusinessModelAnalyzer()
        self.risk_detector = RiskDetectionAgent()
        self.legal_retriever = LegalRetrieverAgent()
        self.checklist_generator = ChecklistGeneratorAgent()

    def analyze_business(self, business_description: str) -> Dict[str, Any]:
        """
        Run the complete compliance analysis workflow.
        
        Args:
            business_description: Detailed description of the business
            
        Returns:
            Dict containing all analysis results including the final checklist
        """
        # Step 1: Analyze business model
        business_analysis = self.business_analyzer.analyze(business_description)
        
        # Step 2: Detect risks
        risk_analysis = self.risk_detector.analyze_risks(
            domain=business_analysis["domain"],
            geography=business_analysis["geography"]
        )
        
        # Step 3: Retrieve legal information
        legal_info = self.legal_retriever.retrieve_legal_info(
            query=f"{business_analysis['domain']} compliance",
            jurisdiction=business_analysis["geography"]
        )
        
        # Step 4: Generate compliance checklist
        checklist = self.checklist_generator.generate_checklist(
            domain=business_analysis["domain"],
            geography=business_analysis["geography"],
            stage="Early-stage",  # This could be made dynamic based on business description
            risks=risk_analysis["risks"],
            legal_docs=legal_info["sources"]
        )
        
        return {
            "business_analysis": business_analysis,
            "risk_analysis": risk_analysis,
            "legal_info": legal_info,
            "compliance_checklist": checklist
        }

# Example usage
if __name__ == "__main__":
    # Initialize the workflow
    workflow = ComplianceWorkflow()
    
    # Example business description
    sample_business = """
    We are a healthtech startup developing a mobile app for remote patient monitoring.
    Our app collects patient health data, provides real-time monitoring, and alerts healthcare providers.
    We plan to operate in the United States, starting with California, and later expand to EU markets.
    Our target users are hospitals and individual healthcare providers.
    """
    
    # Run the complete analysis
    results = workflow.analyze_business(sample_business)
    
    # Print the results
    print("\n=== Business Analysis ===")
    print(f"Domain: {results['business_analysis']['domain']}")
    print(f"Geography: {results['business_analysis']['geography']}")
    
    print("\n=== Risk Analysis ===")
    for risk in results['risk_analysis']['risks']:
        print(f"- {risk}")
    
    print("\n=== Legal Information ===")
    print(f"Summary: {results['legal_info']['summary']}")
    
    print("\n=== Compliance Checklist ===")
    print(results['compliance_checklist']['checklist']) 