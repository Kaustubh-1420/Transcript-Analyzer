import pandas as pd
import os

CSV_FILE = "call_analysis.csv"

def save_to_csv(transcript: str, summary: str, sentiment: str):
    
    row = {
        "Transcript": transcript,
        "Summary": summary,
        "Sentiment": sentiment
    }

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(CSV_FILE, index=False)
    print(f" Saved results to {CSV_FILE}")
