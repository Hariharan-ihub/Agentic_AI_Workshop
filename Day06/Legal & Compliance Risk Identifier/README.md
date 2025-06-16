# Legal & Compliance Risk Identifier

An AI-powered legal risk assessment assistant for early-stage startups. This tool helps founders identify potential legal risks and compliance requirements based on their startup's business model and target markets.

## Features

- Natural language understanding of startup ideas
- Business model classification
- Legal risk detection and flagging
- Customized legal checklists
- Jurisdiction-specific legal resources
- RAG-based document analysis

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

- `app.py`: Main Streamlit application
- `agents/`: Contains different AI agents
  - `startup_classifier.py`: Classifies startup business models
  - `legal_risk.py`: Identifies legal risks
  - `checklist_generator.py`: Generates legal checklists
- `data/`: Contains static data and templates
- `utils/`: Utility functions and helpers

## Usage

1. Enter your startup description in natural language
2. Select target markets/jurisdictions
3. Get comprehensive legal risk assessment and checklist
4. Access relevant legal resources and documentation

## Contributing

Feel free to submit issues and enhancement requests! 