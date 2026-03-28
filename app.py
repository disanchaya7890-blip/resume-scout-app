import streamlit as st
import google.generativeai as genai

# Page Config (Thoda sundar banane ke liye)
st.set_page_config(page_title="AI Resume Scout", layout="centered")

# 1. API Key Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets mein API Key nahi mili!")

# 2. Model Selection (Direct name use kar rahe hain)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("AI Resume Scout")
st.write("Upload your resume text and get AI job suggestions (Free Version)")

# INPUT
resume_text = st.text_area("Paste your resume here", height=200)

# BUTTON
if st.button("Analyze Resume"):
    if resume_text:
        with st.spinner("Analyzing your resume..."):
            try:
                # 3. Content Generation
                response = model.generate_content(
                    f"Analyze this resume and suggest 5 suitable job roles with brief reasons:\n{resume_text}"
                )
                
                # OUTPUT
                st.subheader("Job Suggestions")
                st.markdown(response.text)
                
            except Exception as e:
                # Agar 404 aaye toh alternate model try karega automatically
                st.error(f"Error occurred: {e}")
                st.info("Tip: Check if your requirements.txt has 'google-generativeai'")
    else:
        st.warning("Please enter resume text")
