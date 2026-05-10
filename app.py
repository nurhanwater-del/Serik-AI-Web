# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import requests
import re
import json
import os
import random
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# Баптаулар
st.set_page_config(page_title="Serik-Ai. Твой верный помощник. v1.0", layout="centered")
wikipedia.set_lang("ru")

# Дизайн (CSS)
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    .stTextInput>div>div>input { background-color: #262626; color: white; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #e74c3c; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Serik-Ai. Твой верный помощник. v1.0")

# Жадты жүктеу
if 'memory' not in st.session_state:
    st.session_state.memory = {}

def silent_search(topic):
    data = ""
    queries = [f"{topic} факты описание", f"{topic} история и наука"]
    headers = {'User-Agent': 'Mozilla/5.0'}
    for sq in queries:
        try:
            for url in google_search(sq, num_results=10, lang="ru"):
                try:
                    res = requests.get(url, headers=headers, timeout=3)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    for tag in soup.find_all(['p', 'li']):
                        if len(tag.text) > 45:
                            data += tag.text + " "
                    if len(data) > 8000: break
                except: continue
        except: continue
    return data

# Чат интерфейсі
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Спроси что угодно..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Генерация ответа..."):
            q = prompt.lower().strip()
            if q in st.session_state.memory:
                response = st.session_state.memory[q]
            else:
                topic = q.replace("напиши", "").replace("про", "").strip()
                raw_info = silent_search(topic)
                clean_info = re.sub(r'http\S+|©|На сайте|Источник|Читать далее|\[.*?\]|@\S+|Согласно данным|Сайт', '', raw_info)
                sentences = list(dict.fromkeys([s.strip() for s in clean_info.split('.') if len(s) > 45]))
                
                if len(sentences) > 3:
                    response = ". ".join(sentences[:35]) + "."
                else:
                    response = f"По теме '{topic}' данных недостаточно. Попробуйте другой запрос."
                
                st.session_state.memory[q] = response
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Тазалау батырмасы
if st.sidebar.button("Очистить чат"):
    st.session_state.messages = []
    st.rerun()