# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import requests
import re
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# Беттің баптаулары
st.set_page_config(page_title="Serik-Ai Ultra v2.0", layout="wide")
wikipedia.set_lang("ru")

# ДИЗАЙНДЫ ТҮЗЕТУ: Фон қара, жазу анық АҚ түсті
st.markdown("""
    <style>
    /* Негізгі фон қара */
    .stApp { 
        background-color: #0e1117; 
    }
    /* Барлық мәтінді АҚ түсті қылу */
    .stApp, .stMarkdown, p, h1, h2, h3, span, label {
        color: #ffffff !important;
    }
    /* Сол жақтағы панель (sidebar) баптауы */
    [data-testid="stSidebar"] { 
        background-color: #1a1c23; 
        border-right: 1px solid #30363d; 
    }
    /* Жазу жазатын жердің түсі */
    .stTextInput>div>div>input { 
        background-color: #2d2d2d !important; 
        color: white !important; 
    }
    /* Батырмалардың стилі */
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        background-color: #238636; 
        color: white; 
    }
    </style>
    """, unsafe_allow_html=True)

# Сол жақ панель (Sidebar)
with st.sidebar:
    st.title("🚀 Serik-Ai PRO")
    st.warning("⚠️ ВНИМАНИЕ: Бот анализирует много сайтов. Подождите немного.")
    st.write("---")
    st.markdown("**Что я могу:**")
    st.write("✅ Рефераты (1500+ слов)")
    st.write("✅ Эссе и рассказы")
    st.write("✅ Ответы на вопросы")
    
    if st.button("🗑️ Очистить чат"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Serik-Ai: Твой интеллектуальный автор")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Чатты көрсету (Ақ жазумен)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generate_pro_text(q):
    q = q.lower().strip()
    
    # Режимді анықтау
    mode = "стандарт"
    if "реферат" in q: mode = "реферат"
    elif "эссе" in q: mode = "эссе"
    elif "рассказ" in q or "история" in q: mode = "история"

    topic = q.replace("напиши", "").replace("реферат", "").replace("эссе", "").replace("про", "").replace("рассказ", "").replace("историю", "").strip()

    try:
        all_sentences = []
        # 15 сайтқа дейін іздеу (көлемді болуы үшін)
        search_query = f"{topic} подробный материал статья лекция"
        results = google_search(search_query, num_results=12, lang="ru")
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        for url in results:
            try:
                r = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(r.text, 'html.parser')
                for p in soup.find_all('p'):
                    text = p.get_text().strip()
                    if len(text) > 60:
                        all_sentences.extend(text.split('. '))
            except: continue
        
        unique_sentences = list(dict.fromkeys([s.strip() for s in all_sentences if len(s) > 40]))

        if mode == "реферат":
            res = f"### РЕФЕРАТ: {topic.upper()}\n\n"
            res += "**Введение:** " + ". ".join(unique_sentences[:6]) + ".\n\n"
            res += "**Основная часть:**\n" + ". ".join(unique_sentences[6:60]) + ".\n\n"
            res += "**Заключение:** Таким образом, " + ". ".join(unique_sentences[-4:]) + "."
            return res
        elif mode == "эссе":
            return f"### ЭССЕ: {topic.upper()}\n\n" + ". ".join(unique_sentences[:35]) + "."
        elif mode == "история":
            return f"### ИСТОРИЯ: {topic.upper()}\n\n" + ". ".join(unique_sentences[:30]) + "."
        else:
            return ". ".join(unique_sentences[:20]) + "." if unique_sentences else "Данные не найдены."

    except Exception:
        return "Ошибка при поиске. Попробуйте еще раз."

# Жазу жолағы
if prompt := st.chat_input("Напиши реферат про..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю и пишу..."):
            response = generate_pro_text(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
