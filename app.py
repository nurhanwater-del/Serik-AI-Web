# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import requests
import re
import base64
from gtts import gTTS
import io

# Беттің баптаулары
st.set_page_config(page_title="Serik-Ai PRO Max", layout="wide")
wikipedia.set_lang("ru") # Орысша іздеу

# Дизайн (қара фон, ақ жазу)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stMarkdown, p, h1, h2, h3, span { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Дауыс шығару HTML-ы
def get_audio_html(text):
    try:
        clean_txt = re.sub(r'[^\w\sа-яА-ЯёЁ]', '', text)[:200]
        tts = gTTS(text=clean_txt, lang='ru')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_b64 = base64.b64encode(fp.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_b64}">'
    except: return ""

# Ботпен амандасу
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Привет! Я Serik-Ai. Я всё починил! Теперь я напишу для тебя любой реферат или эссе. Что ищем?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    st.markdown(get_audio_html(welcome), unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_smart_content(q):
    q = q.lower().strip()
    
    # 1. Тез жауаптар
    fast_answers = {
        "привет": "Привет! Я готов к работе. О чем написать?",
        "как дела": "Отлично! Мои сервера работают на полную мощь.",
        "кто тебя создал": "Меня создал гениальный Нұрик!"
    }
    if q in fast_answers: return fast_answers[q]

    # 2. Ақпаратты алу (Википедия арқылы - бұл 100% істейді)
    topic = q.replace("напиши", "").replace("реферат", "").replace("эссе", "").replace("про", "").strip()
    
    try:
        # Бүкіл мақаланы алу
        page = wikipedia.page(topic)
        content = page.content
        summary = page.summary
        
        # Реферат/Эссе форматына салу
        if "реферат" in q:
            sections = content.split('==')
            full_ref = f"### РЕФЕРАТ: {topic.upper()}\n\n"
            full_ref += f"**Введение:** {summary}\n\n"
            full_ref += "**Основная часть:**\n" + content[:5000] + "...\n\n"
            full_ref += "**Заключение:** Данная тема имеет глубокое историческое и социальное значение."
            return full_ref
        
        elif "эссе" in q:
            return f"### ЭССЕ НА ТЕМУ: {topic.upper()}\n\nНа мой взгляд, эта тема очень важна. {summary}"
            
        else:
            return summary
            
    except:
        return f"Я искал информацию про '{topic}', но не смог найти точного совпадения. Попробуй написать название темы точнее."

# Жазу жолағы
if prompt := st.chat_input("Напиши реферат про историю Казахстана..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        response = get_smart_content(prompt)
        st.markdown(response)
        # Жауаптың басын дауыстап оқу
        st.markdown(get_audio_html(response), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
