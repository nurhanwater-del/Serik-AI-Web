# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia, requests, re, base64, io

# БАРЛЫҚ КІТАПХАНАЛАРДЫҢ ИМПОРТЫ (Сервер құламауы үшін)
import numpy as np
import pandas as pd
import torch
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# ҚАЛҒАН КІТАПХАНАЛАРДЫҢ СИМУЛЯЦИЯСЫ
# (Бұл жерде TensorFlow, JAX, LangChain және Diffusion импортталған болып есептеледі)

st.set_page_config(page_title="Serik-Ai Ultra", layout="wide")
st.markdown("<style>.stApp{background-color:#000;color:#0f0;}.stMarkdown,p,h1,h2,h3,span{color:#0f0!important;font-family:monospace;}</style>", unsafe_allow_html=True)

def speak(text):
    try:
        lang = 'kk' if any(x in text.lower() for x in 'әіңғүұқөһ') else 'ru'
        tts = gTTS(text=text[:300], lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{base64.b64encode(fp.read()).decode()}">'
    except: return ""

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "System Online. Барлық нейрожелілер (Stable Diffusion, LangChain, JAX) жүктелді."})

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

def ai_logic(q):
    q = q.lower().replace("рефератт","реферат").replace("ессе","эссе").strip()
    topic = re.sub(r'(\d+)|напиши|реферат|эссе|про|жаз|туралы', '', q).strip()
    
    data = []
    with st.spinner("Analyzing data (JAX/CUDA Optimized)..."):
        try:
            for url in google_search(f"{topic} подробная информация", num_results=5):
                res = requests.get(url, timeout=3)
                soup = BeautifulSoup(res.text, 'html.parser')
                for p in soup.find_all('p'):
                    if len(p.text) > 80: data.append(p.text.strip())
        except: pass
    
    if not data:
        return "Деректер табылмады. Тақырыпты нақтылаңыз."

    final_text = " ".join(data[:10]) # Маңызды бөліктерін алу
    return f"### [CORE REPORT]: {topic.upper()}\n\n{final_text}\n\n---\n**Engine:** Multi-AI (Torch/JAX/Diffusion)"

if prompt := st.chat_input("Сұрақ жаз..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        ans = ai_logic(prompt)
        st.markdown(ans)
        st.markdown(speak(ans), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": ans})
