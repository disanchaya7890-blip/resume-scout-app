import streamlit as st
from openai import OpenAI

# Step 1: Key yahan se hata kar secrets se connect karein
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI Resume Scout")
st.write("Upload your resume text and get AI job suggestions")

# INPUT
resume_text = st.text_area("Paste your resume here")

# BUTTON
if st.button("Analyze Resume"):
    if resume_text:
        # Step 2: Error handling add karein taaki app crash na ho
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"Analyze this resume and suggest suitable jobs:\n{resume_text}"}
                ]
            )
            # OUTPUT
            st.subheader("Job Suggestions")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter resume text")
