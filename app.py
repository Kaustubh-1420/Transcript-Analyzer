import streamlit as st
from groq_client import analyze_transcript
from save_csv import save_to_csv

st.title("Mini Tech Challenge — Transcript Analyzer")

transcript = st.text_area("Enter transcript:")

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

        save_to_csv(transcript, summary, sentiment)
        st.success("Results saved to CSV successfully!")
