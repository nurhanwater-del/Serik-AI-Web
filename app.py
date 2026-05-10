# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import requests
import re
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# Настройка интерфейса
st.set_page_config(page_title="Serik-Ai Ultra v2.0", layout="wide")
wikipedia.set_lang("ru")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #1a1c23; border-right: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #238636; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🚀 Serik-Ai PRO")
    st.info("Бот анализирует до 15 сайтов одновременно для создания глубоких текстов.")
    st.warning("⚠️ Для написания длинных рефератов (1500+ слов) может потребоваться около 30-60 секунд.")
    
    st.write("---")
    st.markdown("**Доступные форматы:**")
    st.write("📝 Реферат (Введение, Части, Заключение)")
    st.write("✒️ Эссе (Личное мнение, Анализ)")
    st.write("📖 Рассказ / История")
    
    if st.button("🗑️ Очистить историю"):
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
    
    # Определение жанра
    mode = "стандарт"
    if "реферат" in q: mode = "реферат"
    elif "эссе" in q: mode = "эссе"
    elif "рассказ" in q or "история" in q: mode = "история"

    topic = q.replace("напиши", "").replace("реферат", "").replace("эссе", "").replace("про", "").replace("рассказ", "").replace("историю", "").strip()

    try:
        # Глубокий сбор данных (до 15 ссылок)
        all_sentences = []
        search_query = f"{topic} подробный материал статья лекция"
        results = google_search(search_query, num_results=15, lang="ru")
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        for url in results:
            try:
                r = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(r.text, 'html.parser')
                paragraphs = soup.find_all('p')
                for p in paragraphs:
                    text = p.get_text().strip()
                    if len(text) > 60 and not any(x in text.lower() for x in ['cookie', 'подпишитесь', 'реклама']):
                        # Очистка и разделение на предложения
                        clean_p = re.sub(r'\[.*?\]', '', text)
                        all_sentences.extend(clean_p.split('. '))
            except: continue
        
        # Уникализация предложений (өздігінен сөйлем құрау үшін)
        unique_sentences = list(dict.fromkeys([s.strip() for s in all_sentences if len(s) > 40]))
        
        if len(unique_sentences) < 10:
            try:
                wiki_data = wikipedia.page(topic).content
                unique_sentences.extend(wiki_data.split('. '))
            except: pass

        # Сборка текста по жанрам
        if mode == "реферат":
            intro = f"### РЕФЕРАТ: {topic.upper()}\n\n**Введение**\n" + ". ".join(unique_sentences[:5]) + "."
            body = "\n\n**Основная часть**\n" + ". ".join(unique_sentences[5:60]) + "."
            outro = "\n\n**Заключение**\n" + "В ходе работы над темой было установлено, что " + ". ".join(unique_sentences[-5:]) + "."
            return intro + body + outro
            
        elif mode == "эссе":
            essay = f"### ЭССЕ: {topic.upper()}\n\n"
            essay += "Рассматривая данную проблему, стоит отметить важное. " + ". ".join(unique_sentences[:40]) + "."
            return essay
            
        elif mode == "история":
            story = f"### ИСТОРИЯ: {topic.upper()}\n\n"
            story += "Это повествование берет свое начало в глубоком анализе событий. " + ". ".join(unique_sentences[:35]) + "."
            return story
            
        else:
            return ". ".join(unique_sentences[:20]) + "."

    except Exception:
        return "Не удалось собрать достаточно данных. Попробуйте уточнить тему запроса."

# Ввод
if prompt := st.chat_input("Напиши подробный реферат про цифровизацию..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Анализирую десятки источников и формирую текст..."):
            response = generate_pro_text(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
