import streamlit as st
from agent import run_travel_agent
from transformers import pipeline

st.set_page_config(page_title="Intelligent Travel Assistant", page_icon="🌍")
st.title("🧳 Intelligent Travel Assistant")

st.write("Enter your travel destination below to get the latest weather and top attractions!")

destination = st.text_input("Enter your travel destination:")

if st.button("Get Info"):
    if destination.strip():
        with st.spinner("Fetching information..."):
            result = run_travel_agent(destination)
        st.markdown(result)
    else:
        st.warning("Please enter a destination.")

def get_weather_fallback(destination: str) -> str:
    prompt = f"Generate a plausible current weather summary for {destination} as if you were a travel assistant."
    generator = pipeline("text-generation", model="gpt2")  # Or use a more suitable model
    result = generator(prompt, max_length=60, num_return_sequences=1)
    return result[0]['generated_text']

def search_attractions_fallback(destination: str) -> str:
    prompt = f"List the top 5 tourist attractions in {destination} with a short description for each."
    generator = pipeline("text-generation", model="gpt2")
    result = generator(prompt, max_length=120, num_return_sequences=1)
    return result[0]['generated_text']

def get_weather(destination: str) -> str:
    # Only use Hugging Face fallback
    return get_weather_fallback(destination)

def search_attractions(destination: str) -> str:
    # Only use Hugging Face fallback
    return search_attractions_fallback(destination) 