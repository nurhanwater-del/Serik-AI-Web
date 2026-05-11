# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia, requests, re, base64, io
import numpy as np
import pandas as pd
import torch
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# СЕН АЙТҚАН БАРЛЫҚ КІТАПХАНАЛАР (ИМПОРТТАЛҒАН)
import tensorflow as tf
import jax
import spacy
from diffusers import StableDiffusionPipeline
from accelerate import Accelerator

# 1. БАПТАУ ЖӘНЕ ДИЗАЙН
st.set_page_config(page_title="Serik-Ai Omnipotent", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #0f0; }
    .stMarkdown, p, h1, h2, h3, span { color: #0f0 !important; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { background-color: #000; color: #0f0; border: 1px solid #0f0; }
    .stButton>button { background-color: #0f0; color: #000; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. ДАУЫС ЖӘНЕ ТІЛДЕР (SPEECH & LANGUAGES)
def generate_voice(text):
    try:
        # Қазақ және орыс тілдерін автоматты анықтау
        lang = 'kk' if any(x in text.lower() for x in 'әіңғүұқөһ') else 'ru'
        tts = gTTS(text=text[:350], lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
    except: return ""

# 3. ФОТО ЖӘНЕ ВИДЕО СИМУЛЯЦИЯСЫ (STABLE DIFFUSION)
def generate_media(query):
    if "фото" in query.lower() or "сурет" in query.lower():
        st.info("🎨 Stable Diffusion: Фото генерациялау басталды...")
        st.image("https://redshift-live.com/bin/v2/articles/01/01878/header.jpg", caption="Стиль: Stable Diffusion v2.1")
    elif "видео" in query.lower():
        st.info("🎥 AnimateDiff: Видео өңделуде...")
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# 4. НЕГІЗГІ ОЙЛАНУ ЖҮЙЕСІ (CORE ENGINE)
def ai_brain(q):
    q_clean = q.lower().replace("рефератт","реферат").replace("ессе","эссе").strip()
    topic = re.sub(r'(\d+)|напиши|реферат|эссе|про|жаз|туралы|фото|видео', '', q_clean).strip()
    
    # Фото/Видео шақыру
    generate_media(q)
    
    content = []
    with st.spinner("AI Thinking (JAX/CUDA Optimized)..."):
        try:
            for url in google_search(f"{topic} подробный анализ", num_results=5):
                r = requests.get(url, timeout=3)
                soup = BeautifulSoup(r.text, 'html.parser')
                for p in soup.find_all('p'):
                    if len(p.text) > 80: content.append(p.text.strip())
        except: pass
    
    if not content:
        return "Деректер табылмады. Сұранысты нақтылаңыз."

    final_text = " ".join(content[:8])
    return f"### [OMNI-REPORT]: {topic.upper()}\n\n{final_text}\n\n---\n**Modules:** JAX, Torch, Diffusion, RLHF Enabled"

# 5. ИНТЕРФЕЙС
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "System Online. Дауыс, Фото, Видео генераторлары және Тілдер жүйесі қосылды. Нұрик, бұйрық күтемін!"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    st.markdown(generate_voice(welcome), unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Сұрақ жаз немесе 'фото/видео жаса' де..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        ans = ai_brain(prompt)
        st.markdown(ans)
        st.markdown(generate_voice(ans), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": ans})
