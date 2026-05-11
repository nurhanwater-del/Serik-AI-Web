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

# БАПТАУЛАР
wikipedia.set_lang("ru")

# ИНТЕРФЕЙС (Кешегі стиль)
st.set_page_config(page_title="Serik-Ai", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #262730; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# ДАУЫС ФУНКЦИЯСЫ
def get_audio_html(text):
    try:
        lang = 'kk' if any(x in text.lower() for x in 'әіңғүұқөһ') else 'ru'
        tts = gTTS(text=text[:250], lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_b64 = base64.b64encode(fp.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_b64}">'
    except:
        return ""

# ЧАТ ТАРИХЫ
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# AI ЛОГИКАСЫ (РЕФЕРАТ ЖӘНЕ ІЗДЕУ)
def ai_engine(query):
    query = query.lower().replace("рефератт", "реферат").replace("ессе", "эссе").strip()
    
    # Сөз санын анықтау
    word_match = re.search(r'(\d+)', query)
    target_words = int(word_match.group(1)) if word_match else 500
    
    # Тақырыпты тазарту
    topic = re.sub(r'(\d+)|напиши|реферат|эссе|про|жаз|туралы', '', query).strip()

    data = []
    with st.spinner(f"Іздеудемін: {topic}..."):
        try:
            # Google-дан ақпарат жинау
            for url in google_search(f"{topic} подробный материал", num_results=5):
                res = requests.get(url, timeout=3)
                soup = BeautifulSoup(res.text, 'html.parser')
                for p in soup.find_all('p'):
                    if len(p.text) > 80:
                        data.append(p.text.strip())
        except:
            pass

    if not data:
        try:
            data = wikipedia.summary(topic, sentences=15).split('. ')
        except:
            return "Кешіріңіз, бұл тақырып бойынша ақпарат табылмады."

    # Мәтінді құрастыру
    final_text = []
    current_count = 0
    while current_count < target_words and len(final_text) < 300:
        for sentence in data:
            if current_count >= target_words: break
            final_text.append(sentence + ". ")
            current_count += len(sentence.split())
        if current_count < target_words: # Ақпарат аз болса қайталау арқылы толтыру
            data = [s + " (толығырақ)" for s in data]

    return f"### {topic.upper()}\n\n" + "".join(final_text)

# ЕНГІЗУ БӨЛІМІ
if prompt := st.chat_input("Тақырыпты жаз (мысалы: Абай Құнанбаев туралы 500 сөз реферат)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ai_engine(prompt)
        st.markdown(response)
        st.markdown(get_audio_html(response), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
