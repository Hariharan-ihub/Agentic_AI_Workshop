# Educational Assessment Generator

This tool uses LangChain and OpenAI's GPT models to generate educational assessments from academic content. It can create concise summaries and multiple-choice questions based on the provided content.

## Features

- Generates 3-5 concise bullet points summarizing the main ideas
- Creates 3-5 multiple-choice questions based on the content
- Each question includes four options and a clearly marked correct answer
- Maintains pedagogical soundness and accuracy

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

```python
from assessment_generator import AssessmentGenerator

# Initialize the generator
generator = AssessmentGenerator()

# Your educational content
content = """
Your educational content here...
"""

# Generate assessment
assessment = generator.generate_assessment(content)

# Access the results
summary = assessment["summary"]
questions = assessment["questions"]
```

## Example Output

The generator will return a dictionary with two main components:

1. Summary: A list of bullet points summarizing the main ideas
2. Questions: A list of multiple-choice questions, each containing:
   - The question text
   - Four options (a, b, c, d)
   - The correct answer

## Requirements

- Python 3.7+
- OpenAI API key
- Required packages (see requirements.txt)

## Note

Make sure to keep your API key secure and never commit it to version control. The `.env` file is included in `.gitignore` by default. 