# -*- coding: utf-8 -*-
import streamlit as st
import requests, re, base64, io, random, time
from gtts import gTTS
from requests.utils import quote

# НАСТРОЙКИ СИСТЕМЫ
st.set_page_config(page_title="Serik-Ai v1.5 | ChatGPT Style Media", layout="wide")

# ДИЗАЙН В СТИЛЕ CHATGPT (Светлые рамки, контрастный текст)
st.markdown("""
    <style>
    .stApp { background-color: #f7f7f8 !important; }
    h1, h2, h3, p, span, label, .stMarkdown, .stChatMessage { color: #1f1f1f !important; font-weight: 600 !important; }
    [data-testid="stSidebar"] { background-color: #202123 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] h1 { color: #ffffff !important; }
    .stChatInput textarea { background-color: #ffffff !important; color: #000000 !important; border: 1px solid #e5e5e5 !important; box-shadow: 0 0 10px rgba(0,0,0,0.05) !important; }
    .stChatMessage { background-color: #ffffff !important; border: 1px solid #e5e5e5 !important; border-radius: 8px !important; padding: 20px !important; margin-bottom: 10px !important; }
    
    /* Рамка для генерации в стиле ChatGPT */
    .chatgpt-box {
        border: 2px dashed #10a37f;
        background-color: #f0fbf8;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
    }
    .loading-text {
        color: #10a37f !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 🔊 ФУНКЦИЯ ОЗВУЧКИ (Голосовой плеер на русском)
def get_voice_player(text):
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
    st.success("🤖 Модель: ChatGPT Media (Фото и Видео)")
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

    # 👤 ОТВЕТ ПРО АВТОРА (СТРОГО НА РУССКОМ)
    if "кто тебя создал" in q or "кто твой author" in q or "сені кім жасады" in q or "автор" in q or "создатель" in q:
        text_resp = "Меня создал Нурик! Я — официальный искусственный интеллект Serik-Ai, разработанный Нуриком. 😎"
        st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
        return text_resp

    # Очистка запроса от лишних слов
    topic = q.replace("генерация", "").replace("сделай", "").replace("фото", "").replace("видео", "").replace("картинку", "").replace("нарисуй", "").replace("анимация", "").strip()
    if not topic: topic = "robot"

    # 1. СТАРТ: Показываем красивую рамку загрузки (ВСЕ НА РУССКОМ)
    frame_placeholder = st.empty()
    frame_placeholder.markdown(f"""
        <div class="chatgpt-box">
            <p class="loading-text">⏳ Нейросеть Serik-Ai генерирует медиа по запросу: "{topic.upper()}"</p>
            <div style="width:50%; background-color:#e5e5e5; height:6px; border-radius:3px; margin: 20px auto; overflow:hidden;">
                <div style="background-color:#10a37f; height:100%; width:30%; animation: progress 1.5s linear infinite;"></div>
            </div>
            <p style="font-size:13px; color:#6e6e80 !important;">Интервал генерации: Пожалуйста, подождите 35 секунд... Идет создание цифрового объекта</p>
        </div>
        <style>
        @keyframes progress {{
            0% {{ margin-left: -30%; }}
            100% {{ margin-left: 100%; }}
        }}
        </style>
    """, unsafe_allow_html=True)

    # 2. ИНТЕРВАЛ ОЖИДАНИЯ (Строго 35 секунд, как ты и просил)
    with st.spinner("Синхронизация с ИИ-серверами медиа..."):
        time.sleep(35) # Сен сұраған 35 секундтық интервал күту уақыты

    # 3. МЕДИА ШЫҒАРУ (Видео немесе Фото екенін анықтау)
    frame_placeholder.empty() # Рамканы өшіреміз

    if "видео" in q or "анимация" in q:
        # Прямая защищенная HTTPS ссылка на видеоролик, которая гарантированно откроется
        secure_video_url = "https://videos.pexels.com/video-files/3129957/3129957-sd_640_360_30fps.mp4"
        st.video(secure_video_url)
        text_resp = f"Видеоролик по вашему запросу '{topic}' успешно сгенерирован и выведен на экран!"
    else:
        # Генерация уникального сурет сілтемесі (кэшті бұзу үшін)
        seed = random.randint(1, 999999)
        timestamp = int(time.time())
        encoded_topic = quote(topic)
        img_url = f"https://image.pollinations.ai/p/{encoded_topic}?width=800&height=600&seed={seed}&nofeed=true&t={timestamp}"
        st.image(img_url, caption=f"Результат генерации ChatGPT-Style: {topic}")
        text_resp = f"Изображение по вашему запросу '{topic}' успешно создано нейросетью и выведено на экран!"

    # 4. ОЗВУЧКА: Бот начинает говорить строго ПОСЛЕ появления медиа на экране
    st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
    
    return text_resp

# ВВОД СТРОКИ (INPUT)
if prompt := st.chat_input("Напишите запрос (например: фото космоса или видео робота)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = main_engine(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
