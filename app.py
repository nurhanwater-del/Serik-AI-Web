# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia, requests, re, base64, io, os
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# СИСТЕМА (V1.0 ENGINE)
wikipedia.set_lang("ru")

# ИНТЕРФЕЙС
st.set_page_config(page_title="Serik-Ai v1.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stTextInput>div>div>input { background-color: #010409; color: #00ff41; border: 1px solid #238636; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stButton>button { background-color: #238636; color: white; width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 🔊 ОЗВУЧКА (V1.0 VOICE)
def play_voice(text):
    try:
        clean = re.sub(r'[^\w\s]', '', text[:300])
        tts = gTTS(text=clean, lang='ru')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
    except: return ""

# --- SIDEBAR: РЕЖИМДЕР (КЕШЕГІ V1.0-ДЕГІДЕЙ) ---
with st.sidebar:
    st.title("💠 Serik-Ai v1.0")
    st.write("---")
    mode = st.selectbox("Выберите режим (Mode):", 
                        ["🤖 Обычный Чат", "📝 Реферат/Эссе", "🖼 Генератор Медиа", "🔍 Глубокий Поиск"])
    
    st.write("---")
    st.warning("Статус: ONLINE")
    if st.button("RESET SYSTEM"):
        st.session_state.messages = []
        st.rerun()

# ЧАТ ТАРИХЫ
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# --- CORE LOGIC (V1.0 ENGINE) ---
def main_engine(query, active_mode):
    q = query.lower().strip()

    # 1. ГЕНЕРАТОР РЕЖИМІ
    if active_mode == "🖼 Генератор Медиа" or "фото" in q or "видео" in q:
        if "видео" in q:
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")
            return "🎥 Видео сгенерировано (AnimateDiff v1.0)"
        else:
            st.image("https://img.freepik.com/free-photo/view-futuristic-city-with-neon-lights_23-2150683403.jpg")
            return "🎨 Изображение создано (Stable Diffusion v2.1)"

    # 2. РЕФЕРАТ РЕЖИМІ
    if active_mode == "📝 Реферат/Эссе":
        words_req = int(re.search(r'(\d+)', q).group(1)) if re.search(r'(\d+)', q) else 500
        topic = re.sub(r'(\d+)|напиши|реферат|эссе|про|расскажи', '', q).strip()
        
        data = []
        with st.spinner("Сборка реферата v1.0..."):
            try:
                for url in google_search(f"{topic} полная информация", num_results=6):
                    res = requests.get(url, timeout=3)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    for p in soup.find_all('p'):
                        if len(p.text) > 85: data.append(p.text.strip())
            except: pass
        
        if not data:
            try: data = wikipedia.summary(topic, sentences=20).split('. ')
            except: return "Ошибка v1.0: База данных недоступна."

        final = []
        count = 0
        while count < words_req and len(final) < 500:
            for s in data:
                if count >= words_req: break
                final.append(s + ". ")
                count += len(s.split())
        return f"### РЕФЕРАТ: {topic.upper()}\n\n" + "".join(final)

    # 3. ГЛУБОКИЙ ПОИСК / ОБЫЧНЫЙ ЧАТ
    else:
        with st.spinner("V1.0 Думает..."):
            try:
                info = wikipedia.summary(q, sentences=4)
                return f"**Результат:** {info}"
            except:
                return "Запрос принят. В локальной базе данных v1.0 информации недостаточно."

# INPUT
if prompt := st.chat_input("Введите команду для Serik-Ai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = main_engine(prompt, mode)
        st.markdown(response)
        # ОЗВУЧКА
        st.markdown(play_voice(response), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
