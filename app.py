import streamlit as st
import pandas as pd
from groq_client import analyze_transcript
from save_csv import save_to_csv
import io

st.title("Mini Tech Challenge — Transcript Analyzer")

# Input
transcript = st.text_area("Enter transcript here:")

if st.button("Analyze"):
    if not transcript.strip():
        st.warning("Please enter a transcript before analyzing.")
    else:
        st.info("Analyzing transcript...")
        summary, sentiment = analyze_transcript(transcript)


        st.subheader("Analysis Results")
        st.write("**Transcript:**", transcript)
        st.write("**Summary:**", summary)
        st.write("**Sentiment:**", sentiment)

        df = pd.DataFrame([{
            "Transcript": transcript,
            "Summary": summary,
            "Sentiment": sentiment
        }])
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        st.download_button(
            label="Download CSV",
            data=csv_buffer.getvalue(),
            file_name="transcript_analysis.csv",
            mime="text/csv"
        )

        save_to_csv(transcript, summary, sentiment)
        st.success("Analysis complete!")
