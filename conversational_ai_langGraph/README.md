# Retail Competitor Analyzer (LangGraph + Gemini + Streamlit)

## Setup

1. Clone the repo
2. Create a `.env` file in the root with:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the app:
   ```sh
   streamlit run app.py
   ```

## Usage
- Enter a query like:
  `Show me clothing store competitors in Koramangala, Bangalore`
- Get a detailed report with competitors, footfall, and strategic insights.

## Notes
- Mock APIs are used for Google Places and footfall. Swap with real APIs as needed.
- All LLM calls use Gemini (Google Generative AI). 