# -*- coding: utf-8 -*-
import streamlit as st
import requests, re, base64, io, random, time
from gtts import gTTS
from requests.utils import quote

# НАСТРОЙКИ СИСТЕМЫ
st.set_page_config(page_title="Serik-Ai v1.5 | Storyline Video Engine", layout="wide")

# ДИЗАЙН В СТИЛЕ CHATGPT
st.markdown("""
    <style>
    .stApp { background-color: #f7f7f8 !important; }
    h1, h2, h3, p, span, label, .stMarkdown, .stChatMessage { color: #1f1f1f !important; font-weight: 600 !important; }
    [data-testid="stSidebar"] { background-color: #202123 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] h1 { color: #ffffff !important; }
    .stChatInput textarea { background-color: #ffffff !important; color: #000000 !important; border: 1px solid #e5e5e5 !important; box-shadow: 0 0 10px rgba(0,0,0,0.05) !important; }
    .stChatMessage { background-color: #ffffff !important; border: 1px solid #e5e5e5 !important; border-radius: 8px !important; padding: 20px !important; margin-bottom: 10px !important; }
    
    .chatgpt-box {
        border: 2px dashed #10a37f;
        background-color: #f0fbf8;
        padding: 25px;
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
    .log-text {
        color: #555555 !important;
        font-family: monospace;
        font-size: 13px;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 🔊 ФУНКЦИЯ ОЗВУЧКИ
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

# БОКОВАЯ ПАНЕЛЬ
with st.sidebar:
    st.title("💠 Serik-Ai v1.5")
    st.write("---")
    st.success("🤖 Режим: Чтение Промптов Кадров")
    st.write("---")
    st.info("Разработчик: Нурик")
    if st.button("Сбросить чат"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# --- ДВИЖОК ИИ ---
def main_engine(query):
    q = query.strip()
    q_low = q.lower()

    # Сұраныстан артық сөздерді тазалау
    clean_topic = q_low.replace("генерация", "").replace("сделай", "").replace("фото", "").replace("видео", "").replace("картинку", "").replace("нарисуй", "").replace("анимация", "").strip()

    # 1. ChatGPT стиліндегі рамка
    frame_placeholder = st.empty()
    
    # Жүктелу барысын түсіндіретін логтар
    logs = [
        "🔍 Шаг 1: Анализ вашего текста и парсинг сюжетной линии...",
        "🧠 Шаг 2: Распознавание отдельных кадров и действий из промпта...",
        "🌐 Шаг 3: Поиск графических соответствий в глубинах интернета...",
        "🎨 Шаг 4: Сборка и компиляция 1-го кадра сценария...",
        "⚡ Шаг 5: Сборка и компиляция 2-го кадра сценария...",
        "🚀 Шаг 6: Сборка и компиляция 3-го кадра сценария...",
        "🛠 Шаг 7: Финальный рендеринг, синхронизация таймингов анимации..."
    ]
    
    for i, log in enumerate(logs):
        frame_placeholder.markdown(f"""
            <div class="chatgpt-box">
                <p class="loading-text">⏳ ИИ Serik-Ai обрабатывает ваш сценарий видео...</p>
                <div style="width:50%; background-color:#e5e5e5; height:6px; border-radius:3px; margin: 15px auto; overflow:hidden;">
                    <div style="background-color:#10a37f; height:100%; width:{(i+1)*14.2}%; transition: width 0.5s;"></div>
                </div>
                <p class="log-text"><b>{log}</b></p>
                <p style="font-size:11px; color:#888888 !important; margin-top:10px;">Прогресс: {int((i+1)*14.2)}%</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(5) # Жалпы 35 секунд күту интервалы

    frame_placeholder.empty()
    timestamp = int(time.time())

    # 2. СЮЖЕТТІ АНЫҚТАУ ЖӘНЕ КАДРЛАРҒА БӨЛУ (Сен жазған промпты оқу)
    # Мәтінді үтір, нүкте немесе сан арқылы бөліп алу логикасы
    user_frames = re.split(r'[,.\n]|\d+:', q)
    user_frames = [f.strip() for f in user_frames if len(f.strip()) > 2]

    # Егер пайдаланушы кадрларды өзі жазса, соны алады, жазбаса автоматты түрде өзі сюжет құрайды
    scenes = []
    if len(user_frames) >= 2:
        for frame in user_frames[:4]: # Ең көп дегенде 4 кадр аламыз
            scenes.append(quote(frame + " cinematic style hyperrealistic"))
    else:
        # Автоматты сюжет (егер жай ғана бір сөз жазса)
        scenes = [
            quote(f"{clean_topic} action scene look around"),
            quote(f"{clean_topic} moving fast dramatic effect"),
            quote(f"{clean_topic} close up powerful background")
        ]

    # Егер сұраныста "фото" немесе "картинка" деген сөз басым болса және сюжет жазылмаса — жай сурет шығады
    if ("фото" in q_low or "картинка" in q_low) and len(user_frames) < 2:
        seed = random.randint(1, 999999)
        img_url = f"https://image.pollinations.ai/p/{quote(clean_topic)}?width=800&height=600&seed={seed}&nofeed=true&t={timestamp}"
        
        photo_html = f"""
        <div style="width:100%; max-width:800px; border-radius:12px; border:3px solid #10a37f; overflow:hidden; box-shadow:0 8px 24px rgba(0,0,0,0.1); margin:auto;">
            <img src="{img_url}" style="width:100%; height:auto; display:block;">
        </div>
        """
        st.markdown(photo_html, unsafe_allow_html=True)
        text_resp = f"Изображение по вашему запросу успешно создано!"
    else:
        # НАҒЫЗ СЮЖЕТТІК ВИДЕО (ӘР КАДРДЫ БӨЛЕК ОҚЫП ҚҰРАСТЫРУ)
        img_urls = []
        for idx, scene in enumerate(scenes):
            seed = random.randint(1, 999999)
            img_urls.append(f"https://image.pollinations.ai/p/{scene}?width=800&height=500&seed={seed}&nofeed=true&t={timestamp+idx}")

        # HTML5/CSS3 арқылы нағыз кадрлық видеоролик жасау (Жай ғана фотоны жақындатпайды, сюжетті ауыстырады)
        slides_html = ""
        animation_duration = len(img_urls) * 4
        
        for idx, url in enumerate(img_urls):
            delay = idx * 4
            slides_html += f'<div class="story-frame" style="background-image:url(\'{url}\'); animation-delay: {delay}s; animation-duration: {animation_duration}s;"></div>'

        video_html = f"""
        <div style="width:100%; max-width:800px; height:500px; position:relative; overflow:hidden; border-radius:12px; border:4px solid #10a37f; box-shadow:0 12px 30px rgba(0,0,0,0.3); margin:auto;">
            {slides_html}
            <div style="position:absolute; bottom:15px; left:20px; background:rgba(16,163,127,0.9); color:#fff; padding:6px 14px; font-family:sans-serif; font-size:12px; border-radius:20px; font-weight:bold; z-index:10;">
                🎬 СЮЖЕТНЫЙ ВИДЕО-ПОТОК ПО ВАШЕМУ СЦЕНАРИЮ
            </div>
        </div>
        <style>
        .story-frame {{
            width:100%; height:100%; position:absolute; top:0; left:0;
            background-size:cover; background-position:center;
            opacity:0;
            animation: playMovie infinite ease-in-out;
        }}
        @keyframes playMovie {{
            0% {{ opacity: 0; }}
            5% {{ opacity: 1; }}
            25% {{ opacity: 1; }}
            30% {{ opacity: 0; }}
            100% {{ opacity: 0; }}
        }}
        </style>
        """
        st.markdown(video_html, unsafe_allow_html=True)
        text_resp = f"Ваш покадровый сценарий успешно распознан! Видеоролик сгенерирован и запущен."

    # 4. ОЗВУЧКА: Медиа шыққан соң ғана сөйлейді
    st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
    return text_resp

# ВВОД СТРОКИ
if prompt := st.chat_input("Напишите сценарий (например: 1: робот бежит, 2: робот летит, 3: робот спит)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = main_engine(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
