import os
import google.generativeai as genai

def gemini_chat(prompt, model="gemini-1.5-flash", max_tokens=512, temperature=0.3):
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model)
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
    )
    return response.text