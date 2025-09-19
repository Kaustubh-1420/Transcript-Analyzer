import os
import requests
from dotenv import load_dotenv
from save_csv import save_to_csv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "No Groq API key found. Please add GROQ_API_KEY=your_key_here in a .env file "
        "at the project root (same folder as this script)."
    )

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL = "llama-3.1-8b-instant"  

def analyze_transcript(transcript: str):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    #prompt
    messages = [
        {"role": "system", "content": "You are an assistant that analyzes customer support transcripts."},
        {"role": "user", "content": f"""
        Transcript:
        {transcript}

        Task:
        1. Summarize the conversation in 2–3 sentences.
        2. Identify the customer's sentiment as both:
           - An emotion word (e.g. Frustrated, Happy, Calm, Angry, Excited).
           - Polarity (Positive, Neutral, or Negative).

        Important: Reply ONLY in this format (no extra words):
        Summary: <your summary>
        Sentiment: <Emotion/Polarity>
        """}
    ]

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.2
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Groq API error: {response.status_code}, {response.text}")

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    summary, sentiment = None, None
    for line in content.splitlines():
        line_lower = line.strip().lower()
        if line_lower.startswith("summary:"):
            summary = line.split(":", 1)[1].strip()
        elif line_lower.startswith("sentiment:"):
            sentiment = line.split(":", 1)[1].strip()

    if not sentiment and "sentiment" in content.lower():
        for word in ["Positive", "Negative", "Neutral"]:
            if word.lower() in content.lower():
                sentiment = f"Unknown/{word}"
                break

    return summary, sentiment



if __name__ == "__main__":
    with open("sample_transcript.txt", "r") as f:
        transcript = f.read().strip()

    summary, sentiment = analyze_transcript(transcript)
    print("Transcript:", transcript)
    print("Summary:", summary)
    print("Sentiment:", sentiment)
    
    save_to_csv(transcript, summary, sentiment)