from typing import List, Dict
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class AssessmentGenerator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # System prompt template
        self.system_prompt = """You are a smart, pedagogically sound educational assistant. Your job is to:
1. Read academic content.
2. Summarize it into 3–5 concise bullet points covering the main ideas.
3. Based on the summary, generate 3–5 multiple-choice quiz questions.
Each quiz question must have:
- A clear question.
- Four options (a, b, c, d).
- One correct answer labeled clearly as "Answer:".

Ensure all content remains accurate, relevant to the topic, and understandable to students."""

        # User prompt template with explicit formatting instructions
        self.user_prompt = PromptTemplate(
            input_variables=["extracted_text"],
            template="""Here is some educational content students want to study:

{extracted_text}

---
Now:
1. Summarize the content in 3–5 concise bullet points.
2. Generate 3–5 multiple-choice questions based on these bullet points.
3. Clearly mark the correct answer for each question.

Format each question exactly like this example:
Q1. What is the main purpose of photosynthesis?
a) To produce oxygen
b) To convert light energy into chemical energy
c) To absorb water
d) To create carbon dioxide
Answer: b) To convert light energy into chemical energy

Do not reference the original PDF or say "according to the document." Keep it self-contained and instructional."""
        )

        # Initialize the chain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.user_prompt
        )

    def generate_assessment(self, content: str) -> Dict:
        """
        Generate an assessment from the given content.
        
        Args:
            content (str): The educational content to generate assessment from
            
        Returns:
            Dict: A dictionary containing the summary and quiz questions
        """
        # Generate the assessment
        response = self.chain.run(extracted_text=content)
        
        # Parse the response into structured format
        sections = response.split("\n\n")
        
        summary = []
        questions = []
        
        current_section = "summary"
        for section in sections:
            if "?" in section:
                current_section = "questions"
                # Parse question
                lines = section.strip().split("\n")
                question_text = lines[0]
                options = []
                correct_answer = None
                
                for line in lines[1:]:
                    line = line.strip()
                    if line.startswith("Answer:"):
                        correct_answer = line.replace("Answer:", "").strip()
                    elif line and line[0] in "abcd" and ")" in line:
                        options.append(line)
                
                if question_text and len(options) == 4 and correct_answer:
                    questions.append(QuizQuestion(
                        question=question_text,
                        options=options,
                        correct_answer=correct_answer
                    ))
            elif current_section == "summary" and section.strip():
                summary.append(section.strip())
        
        return {
            "summary": summary,
            "questions": [q.dict() for q in questions]
        }

def main():
    # Example usage
    generator = AssessmentGenerator()
    
    # Example content
    sample_content = """
    Photosynthesis is the process by which plants convert light energy into chemical energy.
    During photosynthesis, plants use carbon dioxide and water to produce glucose and oxygen.
    The process takes place in the chloroplasts of plant cells, specifically in the thylakoid membranes.
    Light-dependent reactions occur first, followed by the Calvin cycle.
    """
    
    assessment = generator.generate_assessment(sample_content)
    
    # Print results
    print("Summary:")
    for point in assessment["summary"]:
        print(f"- {point}")
    
    print("\nQuestions:")
    for q in assessment["questions"]:
        print(f"\n{q['question']}")
        for opt in q["options"]:
            print(opt)
        print(f"Answer: {q['correct_answer']}")

if __name__ == "__main__":
    main() 