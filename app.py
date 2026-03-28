import streamlit as st
import google.generativeai as genai

# Gemini API setup (Secrets se key uthayega)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("AI Resume Scout")
st.write("Upload your resume text and get AI job suggestions (Free Version)")

# INPUT
resume_text = st.text_area("Paste your resume here")

# BUTTON
if st.button("Analyze Resume"):
    if resume_text:
        try:
            # Gemini response call
            response = model.generate_content(f"Analyze this resume and suggest suitable jobs:\n{resume_text}")
            
            # OUTPUT
            st.subheader("Job Suggestions")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter resume text")
