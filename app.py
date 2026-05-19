# -*- coding: utf-8 -*-
import streamlit as st
import requests, re, base64, io, random, time
from gtts import gTTS

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Serik-Ai v1.5 | Photo Generator", layout="wide")

# ЖЕСТКИЙ КОНТРАСТНЫЙ ДИЗАЙН (Все тексты гарантированно черные и крупные)
st.markdown("""
    <style>
    .stApp { background-color: #f5f7f8 !important; }
    h1, h2, h3, p, span, label, .stMarkdown, .stChatMessage { color: #000000 !important; font-weight: 700 !important; }
    [data-testid="stSidebar"] { background-color: #1a1c1e !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] h1 { color: #ffffff !important; }
    .stChatInput textarea { background-color: #ffffff !important; color: #000000 !important; border: 2px solid #0066cc !important; }
    .stChatMessage { background-color: #ffffff !important; border: 2px solid #dddddd !important; border-radius: 12px !important; padding: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# 🔊 ФУНКЦИЯ ОЗВУЧКИ
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

# БОКОВАЯ ПАНЕЛЬ (SIDEBAR)
with st.sidebar:
    st.title("💠 Serik-Ai v1.5")
    st.write("---")
    st.success("🚀 Режим: Генератор AI Фото")
    st.write("---")
    st.info("Разработчик: Нурик")
    if st.button("Сбросить чат"):
        st.session_state.messages = []
        st.rerun()

# ИСТОРИЯ ЧАТА
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# --- ГЛАВНЫЙ ДВИЖОК ИИ ---
def main_engine(query):
    q = query.lower().strip()

    # 👤 ОТВЕТ ПРО АВТОРА НА РУССКОМ
    if "кто тебя создал" in q or "кто твой автор" in q or "сені кім жасады" in q or "автор" in q or "создатель" in q:
        return "Меня создал Нурик! Я — официальный искусственный интеллект Serik-Ai, разработанный Нуриком. 😎"

    # Очистка текста от лишних слов
    topic = q.replace("генерация", "").replace("сделай", "").replace("фото", "").replace("видео", "").replace("картинку", "").replace("нарисуй", "").replace("анимация", "").strip()
    if not topic: topic = "robot"

    # ТЕК ГАНА ФОТО ГЕНЕРАЦИЯСЫ (ЕШҚАНДАЙ ВИДЕО ЖОҚ)
    with st.spinner("Нейросеть Pollinations AI генерирует новый рисунок..."):
        # Генерация уникального seed и timestamp для обхода кэша Streamlit (әр жолы жаңа сурет шығу үшін)
        seed = random.randint(1, 999999)
        timestamp = int(time.time())
        encoded_topic = requests.utils.quote(topic)
        
        # Ссылка через защищенный HTTPS
        secure_img_url = f"https://image.pollinations.ai/p/{encoded_topic}?width=800&height=600&seed={seed}&nofeed=true&t={timestamp}"
        
        st.image(secure_img_url, caption=f"Сгенерировано ИИ по запросу: {topic}")
        return f"🎨 Изображение по вашему запросу '{topic}' успешно создано нейросетью!"

# ВВОД СТРОКИ (INPUT)
if prompt := st.chat_input("Напишите, что нарисовать (например: робот, приора, космос)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = main_engine(prompt)
        st.markdown(response)
        st.markdown(play_voice(response), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
