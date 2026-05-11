# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import requests
import re
import base64
import io
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# СИСТЕМА БАПТАУЛАРЫ
wikipedia.set_lang("kk")

st.set_page_config(page_title="Серік-Ай AI", layout="wide")

# ДИЗАЙН (КЕШЕГІДЕЙ)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #262730; color: #ffffff; border: 1px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

# --- ДАУЫС ШЫҒАРУ ФУНКЦИЯСЫ (КЕШЕГІДЕЙ) ---
def play_voice(text):
    try:
        # Мәтінді қазақша оқу
        clean_text = re.sub(r'[^\w\s]', '', text[:300]) # Артық символдарды алып тастау
        tts = gTTS(text=clean_text, lang='kk')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_b64 = base64.b64encode(fp.read()).decode()
        # autoplay="true" кешегідей автоматты ойнату үшін
        audio_html = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_b64}">'
        return audio_html
    except Exception as e:
        return f""

# ЧАТ ТАРИХЫ
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# AI ENGINE
def ai_logic(query):
    query = query.lower().strip()
    word_count = int(re.search(r'(\d+)', query).group(1)) if re.search(r'(\d+)', query) else 500
    topic = re.sub(r'(\d+)|жаз|реферат|эссе|туралы|мәлімет|сөз', '', query).strip()

    data = []
    with st.spinner(f"Зерттеу: {topic}..."):
        try:
            for url in google_search(f"{topic} мәлімет", num_results=5):
                res = requests.get(url, timeout=4)
                soup = BeautifulSoup(res.text, 'html.parser')
                for p in soup.find_all('p'):
                    if len(p.text) > 70: data.append(p.text.strip())
        except: pass

    if not data:
        try: data = wikipedia.summary(topic, sentences=15).split('. ')
        except: return "Дерек табылмады."

    result_text = []
    current_words = 0
    while current_words < word_count and len(result_text) < 300:
        for s in data:
            if current_words >= word_count: break
            result_text.append(s + ". ")
            current_words += len(s.split())
        if current_words < word_count: data = [s + " (қосымша дерек)" for s in data]

    return f"### {topic.upper()}\n\n" + "".join(result_text)

# INPUT БӨЛІМІ
if prompt := st.chat_input("Тақырыпты жаз..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ai_logic(prompt)
        st.markdown(response)
        # ДАУЫСТЫ АВТОМАТТЫ ТҮРДЕ ҚОСУ
        st.markdown(play_voice(response), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
