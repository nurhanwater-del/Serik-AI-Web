# -*- coding: utf-8 -*-
import streamlit as st
import requests, re, base64, io, random, time
from gtts import gTTS
from requests.utils import quote

# НАСТРОЙКИ СИСТЕМЫ
st.set_page_config(page_title="Serik-Ai v1.5 | Professional Video Engine", layout="wide")

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
    st.success("🤖 Движок: Безбарьерный Видео-Поток")
    st.write("---")
    st.info("Разработчик: Нурик")
    if st.button("Сбросить чат"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# --- ГЛАВНЫЙ ДВИЖОК ИИ ---
def main_engine(query):
    q = query.strip()
    q_low = q.lower()

    clean_topic = q_low.replace("генерация", "").replace("сделай", "").replace("фото", "").replace("видео", "").replace("картинку", "").replace("нарисуй", "").replace("анимация", "").strip()

    # 1. ChatGPT стиліндегі рамка мен логтар
    frame_placeholder = st.empty()
    logs = [
        "🔍 Шаг 1: Парсинг и семантический анализ вашего сценария...",
        "🧠 Шаг 2: Разделение промпта на независимые экшен-кадры...",
        "🌐 Шаг 3: Поиск высокоточных графических ресурсов в сети...",
        "🎨 Шаг 4: Интеграция 1-го кадра и стабилизация базового фона...",
        "⚡ Шаг 5: Инициализация 2-го кадра с наложением эффекта движения...",
        "🚀 Шаг 6: Финализация 3-го кадра и рендеринг бесшовной анимации...",
        "🛠 Шаг 7: Сборка медиа-потока. Устранение мерцания и белых экранов..."
    ]
    
    for i, log in enumerate(logs):
        frame_placeholder.markdown(f"""
            <div class="chatgpt-box">
                <p class="loading-text">⏳ Нейросеть Serik-Ai компилирует бесшовное видео...</p>
                <div style="width:50%; background-color:#e5e5e5; height:6px; border-radius:3px; margin: 15px auto; overflow:hidden;">
                    <div style="background-color:#10a37f; height:100%; width:{(i+1)*14.2}%; transition: width 0.5s;"></div>
                </div>
                <p class="log-text"><b>{log}</b></p>
                <p style="font-size:11px; color:#888888 !important; margin-top:10px;">Прогресс: {int((i+1)*14.2)}%</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(5) # 35 секунд күту уақыты

    frame_placeholder.empty()
    timestamp = int(time.time())

    # Мәтінді кадрларға бөлу
    user_frames = re.split(r'[,.\n]|\d+:', q)
    user_frames = [f.strip() for f in user_frames if len(f.strip()) > 2]

    scenes = []
    if len(user_frames) >= 2:
        for frame in user_frames[:3]: # Тұрақты жұмыс үшін 3 негізгі кадр аламыз
            scenes.append(quote(frame + " cinematic dynamic action 8k"))
    else:
        scenes = [
            quote(f"{clean_topic} cinematic movement epic action shot"),
            quote(f"{clean_topic} close up cyber details glowing effects"),
            quote(f"{clean_topic} fast flying moving through environment")
        ]

    if ("фото" in q_low or "картинка" in q_low) and len(user_frames) < 2:
        seed = random.randint(1, 999999)
        img_url = f"https://image.pollinations.ai/p/{quote(clean_topic)}?width=800&height=600&seed={seed}&nofeed=true&t={timestamp}"
        
        photo_html = f"""
        <div style="width:100%; max-width:800px; border-radius:12px; border:3px solid #10a37f; overflow:hidden; box-shadow:0 8px 24px rgba(0,0,0,0.1); margin:auto;">
            <img src="{img_url}" style="width:100%; height:auto; display:block;">
        </div>
        """
        st.markdown(photo_html, unsafe_allow_html=True)
        text_resp = f"Изображение по вашему запросу успешно выведено на экран!"
    else:
        # СЮЖЕТТІК ВИДЕО (АҚ ФОНСЫЗ ЖӘНЕ ДИНАМИКАЛЫҚ ҚОЗҒАЛЫСПЕН)
        img_urls = []
        for idx, scene in enumerate(scenes):
            seed = random.randint(1, 999999)
            img_urls.append(f"https://image.pollinations.ai/p/{scene}?width=800&height=500&seed={seed}&nofeed=true&t={timestamp+idx}")

        # Егер суреттер әлі жүктеліп үлгермесе, ақ фон шықпас үшін контейнердің өзіне бірінші суретті бекітеміз
        video_html = f"""
        <div style="width:100%; max-width:800px; height:500px; position:relative; overflow:hidden; border-radius:12px; border:4px solid #10a37f; box-shadow:0 12px 30px rgba(0,0,0,0.3); margin:auto; background-image:url('{img_urls[0]}'); background-size:cover; background-position:center;">
            <div class="pro-frame f1" style="background-image:url('{img_urls[0]}');"></div>
            <div class="pro-frame f2" style="background-image:url('{img_urls[1]}');"></div>
            <div class="pro-frame f3" style="background-image:url('{img_urls[2]}');"></div>
            <div style="position:absolute; bottom:15px; left:20px; background:rgba(16,163,127,0.95); color:#fff; padding:6px 14px; font-family:sans-serif; font-size:12px; border-radius:20px; font-weight:bold; z-index:99;">
                🎬 СЮЖЕТНЫЙ ВИДЕО-ПОТОК SERIK-AI
            </div>
        </div>
        <style>
        .pro-frame {{
            width:100%; height:100%; position:absolute; top:0; left:0;
            background-size:cover; background-position:center;
            opacity:0;
        }}
        /* Нағыз кино сияқты қозғалыс пен біркелкі бесшовный ауысу анимациясы */
        .f1 {{ animation: playF1 15s infinite ease-in-out; }}
        .f2 {{ animation: playF2 15s infinite ease-in-out; }}
        .f3 {{ animation: playF3 15s infinite ease-in-out; }}

        @keyframes playF1 {{
            0% {{ opacity: 1; transform: scale(1.0) translateX(0px); }}
            30% {{ opacity: 1; transform: scale(1.04) translateX(10px); }}
            33% {{ opacity: 0; }}
            100% {{ opacity: 0; }}
        }}
        @keyframes playF2 {{
            0% {{ opacity: 0; }}
            33% {{ opacity: 1; transform: scale(1.0); }}
            63% {{ opacity: 1; transform: scale(1.05); }}
            66% {{ opacity: 0; }}
            100% {{ opacity: 0; }}
        }}
        @keyframes playF3 {{
            0% {{ opacity: 0; }}
            66% {{ opacity: 1; transform: scale(1.05); }}
            96% {{ opacity: 1; transform: scale(1.0) translateY(10px); }}
            100% {{ opacity: 0; }}
        }}
        </style>
        """
        st.markdown(video_html, unsafe_allow_html=True)
        text_resp = f"Сюжетный видеоролик успешно собран из разных экшен-сцен без мерцания экранов!"

    st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
    return text_resp

# ВВОД СТРОКИ
if prompt := st.chat_input("Напишите сценарий (например: робот бежит, робот стреляет, робот улетает)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = main_engine(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
