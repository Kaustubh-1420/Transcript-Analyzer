from groq_client import analyze_transcript
from save_csv import save_to_csv

def main():
    print("Mini Tech Challenge — Transcript Analyzer")
    transcript = input("Enter transcript: ").strip()

    if not transcript:
        print("No transcript entered. Exiting.")
        return

    print("\n Analyzing transcript...")
    summary, sentiment = analyze_transcript(transcript)

    print("\n=== Analysis Results ===")
    print("Transcript:", transcript)
    print("Summary:", summary)
    print("Sentiment:", sentiment)

    save_to_csv(transcript, summary, sentiment)


if __name__ == "__main__":
    main()
