import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- CONFIGURATION ---
# App ka title aur layout set karna
st.set_page_config(page_title="BharatPurity AI - Pro", layout="wide")

# Stitch ke Secrets se API Key lena
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Please set your GEMINI_API_KEY in Stitch Secrets.")

# --- MULTILINGUAL DICTIONARY[cite: 1] ---
translations = {
    "English": {
        "title": "BharatPurity AI Pro",
        "upload": "Upload an image (Vegetables, Milk, Grains)",
        "btn_analyze": "Run Purity Check",
        "chat_header": "Ask AI about this item",
        "pay_header": "Upgrade to Premium",
        "report_btn": "Download Purity Report",
        "purity_score": "Purity Score",
        "analysis_placeholder": "Analysis will appear here...",
        "premium_msg": "Get unlimited scans & PDF reports for ₹499/month"
    },
    "Hindi": {
        "title": "भारतप्यूरिटी AI प्रो",
        "upload": "तस्वीर अपलोड करें (सब्जियां, दूध, अनाज)",
        "btn_analyze": "शुद्धता की जांच करें",
        "chat_header": "इस आइटम के बारे में AI से पूछें",
        "pay_header": "प्रीमियम में अपग्रेड करें",
        "report_btn": "शुद्धता रिपोर्ट डाउनलोड करें",
        "purity_score": "शुद्धता स्कोर",
        "analysis_placeholder": "विश्लेषण यहाँ दिखाई देगा...",
        "premium_msg": "₹499/माह में असीमित स्कैन और PDF रिपोर्ट प्राप्त करें"
    },
    "German": {
        "title": "BharatPurity KI Pro",
        "upload": "Bild hochladen (Gemüse, Milch, Getreide)",
        "btn_analyze": "Reinheitsprüfung durchführen",
        "chat_header": "Fragen Sie die KI zu diesem Artikel",
        "pay_header": "Upgrade auf Premium",
        "report_btn": "Reinheitsbericht herunterladen",
        "purity_score": "Reinheitswert",
        "analysis_placeholder": "Analyse wird hier angezeigt...",
        "premium_msg": "Unbegrenzte Scans & PDF-Berichte für 5,99 €/Monat"
    }
}

# --- UI SETUP ---
# Sidebar mein language select karne ka option[cite: 1]
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi", "German"])
t = translations[lang]

st.title(t["title"])
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(t["upload"])
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button(t["btn_analyze"]):
            with st.spinner("Processing..."):
                # Vision logic jo milk/veg/purity scan karta hai[cite: 1]
                prompt = f"Analyze this image for purity and safety. Category: Vegetable/Milk/Food. Language: {lang}. Provide a purity score out of 100."
                response = model.generate_content([prompt, img])
                st.session_state['result'] = response.text
                st.session_state['has_analyzed'] = True

with col2:
    if 'result' in st.session_state:
        st.subheader("Analysis Result")
        st.info(st.session_state['result'])
        
        # DOWNLOAD REPORT FEATURE[cite: 1]
        report_text = f"BharatPurity AI Report\nLanguage: {lang}\nResult: {st.session_state['result']}"
        st.download_button(t["report_btn"], data=report_text, file_name="purity_report.txt")
    else:
        st.write(t["analysis_placeholder"])

# --- CHATBOT COMMUNICATION LAYER[cite: 1] ---
st.markdown("---")
st.subheader(t["chat_header"])
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history dikhana
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User se input lena
if chat_input := st.chat_input("Ask a follow-up..."):
    st.session_state.messages.append({"role": "user", "content": chat_input})
    with st.chat_message("user"):
        st.write(chat_input)
    
    # AI ko pichle scan ka context dena
    context = st.session_state.get('result', '')
    full_prompt = f"Previous Analysis: {context}. User Question: {chat_input}. Answer in {lang}."
    ai_response = model.generate_content(full_prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_response.text})
    with st.chat_message("assistant"):
        st.write(ai_response.text)

# --- MONETIZATION (PAYMENT BUTTON)[cite: 1, 2] ---
st.sidebar.markdown("---")
st.sidebar.subheader(t["pay_header"])
st.sidebar.write(t["premium_msg"])

# Yahan apna Stripe payment link paste karein
payment_url = "https://buy.stripe.com/test_payment_link" 
st.sidebar.markdown(f'''
<a href="{payment_url}" target="_blank">
    <button style="width:100%; background-color:#28a745; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">
        Get Premium Now
    </button>
</a>
''', unsafe_allow_html=True)
