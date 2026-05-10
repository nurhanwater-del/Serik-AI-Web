# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import requests
import re
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# Баптаулар
st.set_page_config(page_title="Serik-Ai Ultra v2.0", layout="wide")
wikipedia.set_lang("ru")

# Дизайн: Жазулар анық АҚ түсті болуы үшін
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stApp, .stMarkdown, p, h1, h2, h3, span, label { color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #1a1c23; border-right: 1px solid #30363d; }
    .stTextInput>div>div>input { background-color: #2d2d2d !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🚀 Serik-Ai PRO")
    st.warning("⚠️ Если текст пустой, попробуйте уточнить запрос.")
    if st.button("🗑️ Очистить чат"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Serik-Ai: Твой интеллектуальный автор")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generate_pro_text(q):
    q = q.lower().strip()
    mode = "стандарт"
    if "реферат" in q: mode = "реферат"
    elif "эссе" in q: mode = "эссе"
    
    topic = q.replace("напиши", "").replace("реферат", "").replace("эссе", "").replace("про", "").strip()

    try:
        # 1. Тез арада Википедиядан ақпарат алу (бос қалмау үшін)
        wiki_text = ""
        try:
            wiki_text = wikipedia.summary(topic, sentences=10)
        except:
            pass

        # 2. Гуглдан қосымша мәтін жинау
        all_sentences = []
        search_query = f"{topic} история факты подробно"
        results = google_search(search_query, num_results=10, lang="ru")
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        for url in results:
            try:
                r = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(r.text, 'html.parser')
                for p in soup.find_all('p'):
                    t = p.get_text().strip()
                    if len(t) > 60: all_sentences.append(t)
            except: continue
        
        # Сөйлемдерді біріктіру
        full_data = list(dict.fromkeys(all_sentences))
        
        # Егер Гуглдан ештеңе табылмаса, Википедияны қолдану
        if not full_data and wiki_text:
            full_data = wiki_text.split('. ')

        if len(full_data) < 3:
            return f"По теме '{topic}' в сети мало информации. Попробуйте написать по-другому (например: 'История СССР')."

        # Мәтінді құрастыру
        if mode == "реферат":
            res = f"### РЕФЕРАТ: {topic.upper()}\n\n"
            res += f"**Введение:** {full_data[0]}.\n\n"
            res += "**Основная часть:** " + ". ".join(full_data[1:25]) + ".\n\n"
            res += f"**Заключение:** Таким образом, изучение {topic} показывает его важность в истории."
            return res
        else:
            return ". ".join(full_data[:15]) + "."

    except Exception:
        return "Ошибка поиска. Попробуйте уточнить запрос."

if prompt := st.chat_input("Напиши реферат про..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Пишу подробный текст..."):
            response = generate_pro_text(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
