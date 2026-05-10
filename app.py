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

# Настройка страницы
st.set_page_config(page_title="Serik-Ai Ultra PRO", layout="wide")
wikipedia.set_lang("ru")

# Дизайн: Қара фон, ақ жазу
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stApp, p, h1, h2, h3, span, label { color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #1a1c23; border-right: 1px solid #30363d; }
    .stTextInput>div>div>input { background-color: #2d2d2d !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Дауыс функциясы (Тек қысқаша оқу үшін)
def speak_text(text):
    clean_txt = re.sub(r'[^\w\sа-яА-ЯёЁ]', '', text)[:250] # Тек алғашқы 250 әріпті оқиды
    tts = gTTS(text=clean_txt, lang='ru')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

with st.sidebar:
    st.title("🧠 Serik-Ai Ultra PRO")
    st.markdown("---")
    st.success("✅ Статус: Работает")
    st.info("📢 Бот умеет писать огромные рефераты и озвучивать краткую информацию.")
    
    # Дауысты қосу/өшіру баптауы
    voice_on = st.checkbox("Включить озвучку ответа", value=True)
    
    if st.button("🗑️ Очистить историю"):
        st.session_state.messages = []
        st.rerun()

# Боттың өзін таныстыруы (Кіргенде бір рет шығады)
if "messages" not in st.session_state or not st.session_state.messages:
    intro_text = "Привет! Я Serik-Ai, твой мощный интеллект. Я могу написать огромный реферат, эссе или историю. Просто напиши тему!"
    st.session_state.messages = [{"role": "assistant", "content": intro_text}]

st.title("🤖 Serik-Ai: Генератор контента")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_mega_response(q):
    q = q.lower().strip()
    
    # Жанрларды анықтау
    mode = "стандарт"
    if "реферат" in q: mode = "реферат"
    elif "эссе" in q: mode = "эссе"
    elif "рассказ" in q or "история" in q: mode = "история"

    topic = q.replace("напиши", "").replace("реферат", "").replace("эссе", "").replace("про", "").replace("рассказ", "").replace("историю", "").strip()

    try:
        all_data = []
        # Гуглдан 20 сайтқа дейін терең іздеу (көлемді болуы үшін)
        results = google_search(f"{topic} подробный анализ лекция википедия", num_results=15, lang="ru")
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        for url in results:
            try:
                r = requests.get(url, headers=headers, timeout=4)
                soup = BeautifulSoup(r.text, 'html.parser')
                for p in soup.find_all('p'):
                    t = p.get_text().strip()
                    if len(t) > 80: all_data.append(t)
                if len(all_data) > 150: break 
            except: continue
        
        # Мәтінді құрастыру (1500-2000 сөзге жақындату)
        if len(all_data) < 5:
            try:
                wiki_p = wikipedia.page(topic).content
                all_data.extend(wiki_p.split('. '))
            except: pass

        if mode == "реферат":
            res = f"### ПОЛНЫЙ РЕФЕРАТ: {topic.upper()}\n\n"
            res += "**ВВЕДЕНИЕ:** " + ". ".join(all_data[:10]) + ".\n\n"
            res += "**ГЛАВА 1:** " + ". ".join(all_data[10:40]) + ".\n\n"
            res += "**ГЛАВА 2:** " + ". ".join(all_data[40:80]) + ".\n\n"
            res += "**ГЛАВА 3:** " + ". ".join(all_data[80:120]) + ".\n\n"
            res += "**ЗАКЛЮЧЕНИЕ:** " + ". ".join(all_data[-10:]) + "."
            return res
        elif mode == "эссе":
            return f"### ЭССЕ: {topic.upper()}\n\n" + ". ".join(all_data[:60]) + "."
        elif mode == "история":
            return f"### ИСТОРИЯ: {topic.upper()}\n\n" + ". ".join(all_data[:50]) + "."
        else:
            return ". ".join(all_data[:30]) + "."

    except Exception:
        return "Не удалось собрать данные. Попробуйте другой запрос."

# Жазу
if prompt := st.chat_input("Напиши огромный реферат про..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Собираю тысячи слов из интернета..."):
            response = get_mega_response(prompt)
            st.markdown(response)
            
            # Дауыс шығару (Егер қосулы болса)
            if voice_on:
                audio_fp = speak_text(response)
                st.audio(audio_fp, format='audio/mp3')
                
            st.session_state.messages.append({"role": "assistant", "content": response})
