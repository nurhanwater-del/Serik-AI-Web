# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import requests
import re
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# Баптаулар
st.set_page_config(page_title="Serik-Ai v1.0", layout="centered")
wikipedia.set_lang("ru")

st.title("🤖 Serik-Ai. Твой верный помощник. v1.0")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Чат тарихын көрсету
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_smart_response(q):
    q = q.lower().strip()
    
    # 1. Қарапайым сұрақтарға жауап (Сәлемдесу)
    greetings = {
        "привет": "Привет! Я Serik-Ai. О чем хочешь узнать сегодня?",
        "как дела": "У меня все отлично! Готов искать для тебя информацию.",
        "кто ты": "Я твой личный помощник Serik-Ai, созданный для поиска знаний.",
        "что ты умеешь": "Я могу найти информацию о чем угодно: от истории до технологий."
    }
    
    if q in greetings:
        return greetings[q]

    # 2. Интернеттен іздеу
    try:
        topic = q.replace("напиши", "").replace("про", "").strip()
        data = ""
        # Іздеуді күшейту
        search_results = google_search(f"{topic} это подробно википедия", num_results=8, lang="ru")
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        for url in search_results:
            try:
                res = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(res.text, 'html.parser')
                for tag in soup.find_all('p'):
                    if len(tag.text) > 50:
                        data += tag.text + " "
                if len(data) > 5000: break
            except: continue
        
        # Тазалау
        clean_text = re.sub(r'http\S+|©|Источник|\[.*?\]', '', data)
        sentences = [s.strip() for s in clean_text.split('.') if len(s) > 40]
        
        if len(sentences) > 2:
            return ". ".join(sentences[:25]) + "."
        else:
            # Егер ештеңе таппаса, Википедияны тексеру
            try:
                return wikipedia.summary(topic, sentences=5)
            except:
                return f"Я искал информацию про '{topic}', но на сайтах пока мало данных. Попробуй спросить по-другому."
    except:
        return "Произошла ошибка при поиске. Пожалуйста, попробуй позже."

# Жаңа хабарлама жіберу
if prompt := st.chat_input("Спроси что угодно..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = get_smart_response(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
