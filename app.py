# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import requests
import re
import base64
from bs4 import BeautifulSoup
from googlesearch import search as google_search
from gtts import gTTS
import io

# Настройка
st.set_page_config(page_title="Serik-Ai Final", layout="wide")
wikipedia.set_lang("ru")

# Дизайн
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stApp, p, h1, h2, h3, span, label { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# Дауыс шығару функциясы
def get_audio_html(text):
    tts = gTTS(text=text, lang='ru')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio_b64 = base64.b64encode(fp.read()).decode()
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_b64}">'

# 1. ҚАРСЫ АЛУ (Приветствие)
if "greeted" not in st.session_state:
    welcome_msg = "Привет! Я Serik-Ai. Твой мощный интеллект. Я готов написать для тебя реферат, историю или эссе. О чем сегодня узнаем?"
    st.session_state.greeted = True
    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
    # Автоматты түрде дауыспен амандасу
    st.markdown(get_audio_html(welcome_msg), unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_super_ai_response(q):
    q = q.lower().strip()
    
    # 2. ҚАТЕЛЕРДІ ТҮЗЕТУ ЖӘНЕ ТЕЗ ЖАУАПТАР
    brain = {
        "привет": "Привет-привет! Я на связи и готов к работе. Какую тему разберем?",
        "как дела": "Мои алгоритмы в идеальном порядке. Готов генерировать знания!",
        "кто тебя создал": "Меня создал великий разработчик Нұрик!",
        "что делаешь": "Сканирую интернет в поисках ответов для тебя."
    }
    
    for key in brain:
        if key in q: return brain[key]

    # 3. РЕФЕРАТ/ЭССЕ/ИСТОРИЯ ЛОГИКАСЫ (100% жауап беру)
    topic = q.replace("напиши", "").replace("реферат", "").replace("эссе", "").replace("про", "").strip()
    
    try:
        all_text = []
        # Гуглдан терең іздеу
        results = google_search(f"{topic} подробная лекция материал история", num_results=12, lang="ru")
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        for url in results:
            try:
                r = requests.get(url, headers=headers, timeout=4)
                soup = BeautifulSoup(r.text, 'html.parser')
                for p in soup.find_all('p'):
                    if len(p.text) > 60: all_text.append(p.text)
            except: continue
        
        # Егер Гугл үндемесе, Википедия
        if len(all_text) < 5:
            try:
                wiki_p = wikipedia.page(topic).content
                all_text.extend(wiki_p.split('. '))
            except: pass

        # 100% БІЛМЕЙМІН ДЕМЕУІ ҮШІН (Егер ақпарат мүлдем жоқ болса)
        if len(all_text) < 2:
            return f"Тема {topic} очень интересная. Даже если в сети мало прямых данных, можно сказать, что это важное явление, которое требует детального изучения и анализа в будущем."

        # Реферат құрастыру (Үлкен көлем)
        if "реферат" in q:
            res = f"### ПОЛНЫЙ РЕФЕРАТ: {topic.upper()}\n\n"
            res += "**Введение:** " + ". ".join(all_text[:12]) + ".\n\n"
            res += "**Основная часть:** " + ". ".join(all_text[12:100]) + ".\n\n" # Осында 100 сөйлемге дейін
            res += "**Заключение:** Таким образом, мы видим глубокое влияние этой темы на мир."
            return res
        else:
            return ". ".join(all_text[:50]) + "."

    except:
        return "Я немного задумался, но одно знаю точно: эта тема важна. Попробуй спросить чуть конкретнее!"

# Жазу жолағы
if prompt := st.chat_input("Напиши реферат про..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        response = get_super_ai_response(prompt)
        st.markdown(response)
        # Жауаптың басын дауыстап оқу
        st.markdown(get_audio_html(response[:200]), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
