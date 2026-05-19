# -*- coding: utf-8 -*-
import streamlit as st
import requests, re, base64, io, random, time
from gtts import gTTS
from requests.utils import quote

# НАСТРОЙКИ СИСТЕМЫ
st.set_page_config(page_title="Serik-Ai v1.5 | Autonomous Media Engine", layout="wide")

# ДИЗАЙН В СТИЛЕ CHATGPT (Светлые рамки, черный контрастный текст)
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
    st.success("🤖 Движок: Автономный ИИ-Медиа")
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

    # 👤 ОТВЕТ ПРО АВТОРА
    if "кто тебя создал" in q or "кто твой автор" in q or "сені кім жасады" in q or "автор" in q or "создатель" in q:
        text_resp = "Меня создал Нурик! Я — официальный искусственный интеллект Serik-Ai, разработанный Нуриком. 😎"
        st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
        return text_resp

    # Очистка запроса от лишних слов
    topic = q.replace("генерация", "").replace("сделай", "").replace("фото", "").replace("видео", "").replace("картинку", "").replace("нарисуй", "").replace("анимация", "").strip()
    if not topic: topic = "robot"

    # 1. СТАРТ: Показываем красивую рамку загрузки ChatGPT (ВСЕ НА РУССКОМ)
    frame_placeholder = st.empty()
    frame_placeholder.markdown(f"""
        <div class="chatgpt-box">
            <p class="loading-text">⏳ Нейросеть Serik-Ai автономно собирает кадры и создает объект: "{topic.upper()}"</p>
            <div style="width:50%; background-color:#e5e5e5; height:6px; border-radius:3px; margin: 20px auto; overflow:hidden;">
                <div style="background-color:#10a37f; height:100%; width:30%; animation: progress 1.5s linear infinite;"></div>
            </div>
            <p style="font-size:13px; color:#6e6e80 !important;">Интервал компиляции: Подождите 35 секунд... ИИ самостоятельно верстает медиа-поток</p>
        </div>
        <style>
        @keyframes progress {{
            0% {{ margin-left: -30%; }}
            100% {{ margin-left: 100%; }}
        }}
        </style>
    """, unsafe_allow_html=True)

    # 2. ИНТЕРВАЛ ОЖИДАНИЯ (Строго 35 секунд для симуляции верстки и компиляции)
    with st.spinner("Поиск и компиляция графических элементов..."):
        time.sleep(35)

    # 3. МЕДИА ШЫҒАРУ (Өздігінен құрастыру кезеңі)
    frame_placeholder.empty() # Рамканы тазалаймыз
    timestamp = int(time.time())
    encoded_topic = quote(topic)

    if "видео" in q or "анимация" in q:
        # ВИДЕО СҰРАЛҒАНДА: ИИ 4 түрлі бағыттағы суретті тауып, өзі нағыз видеоролик құрастырады
        seed1 = random.randint(1, 250000)
        seed2 = random.randint(251000, 500000)
        seed3 = random.randint(501000, 750000)
        seed4 = random.randint(751000, 999999)
        
        # 4 кадрды әр түрлі стильде алдыру (кэшті толық бұзу)
        img1 = f"https://image.pollinations.ai/p/{encoded_topic}_close_up?width=800&height=500&seed={seed1}&nofeed=true&t={timestamp}"
        img2 = f"https://image.pollinations.ai/p/{encoded_topic}_cinematic?width=800&height=500&seed={seed2}&nofeed=true&t={timestamp+1}"
        img3 = f"https://image.pollinations.ai/p/{encoded_topic}_cyberpunk?width=800&height=500&seed={seed3}&nofeed=true&t={timestamp+2}"
        img4 = f"https://image.pollinations.ai/p/{encoded_topic}_epic?width=800&height=500&seed={seed4}&nofeed=true&t={timestamp+3}"
        
        # HTML5 / CSS3 слайд-видео ойнатқышы. Суреттер бір-біріне масштабталып, әдемі ағып ауысады
        video_html = f"""
        <div style="width:100%; max-width:800px; height:500px; position:relative; overflow:hidden; border-radius:12px; border:4px solid #10a37f; box-shadow:0 12px 30px rgba(0,0,0,0.2); margin:auto;">
            <div class="v-slide" style="background-image:url('{img1}'); animation-delay: 0s;"></div>
            <div class="v-slide" style="background-image:url('{img2}'); animation-delay: 4s;"></div>
            <div class="v-slide" style="background-image:url('{img3}'); animation-delay: 8s;"></div>
            <div class="v-slide" style="background-image:url('{img4}'); animation-delay: 12s;"></div>
            <div style="position:absolute; bottom:15px; left:20px; background:rgba(16,163,127,0.85); color:#fff; padding:6px 14px; font-family:sans-serif; font-size:12px; border-radius:20px; font-weight:bold; letter-spacing:0.5px;">
                🎬 АВТОНОМНЫЙ ВИДЕО-ПОТОК SERIK-AI: {topic.upper()}
            </div>
        </div>
        <style>
        .v-slide {{
            width:100%; height:100%; position:absolute; top:0; left:0;
            background-size:cover; background-position:center;
            opacity:0; transform: scale(1);
            animation: flowVideo 16s infinite ease-in-out;
        }}
        @keyframes flowVideo {{
            0% {{ opacity: 0; transform: scale(1.0); }}
            4% {{ opacity: 1; }}
            25% {{ opacity: 1; transform: scale(1.04); }}
            29% {{ opacity: 0; transform: scale(1.06); }}
            100% {{ opacity: 0; }}
        }}
        </style>
        """
        st.markdown(video_html, unsafe_allow_html=True)
        text_resp = f"Видеоролик по вашему запросу '{topic}' успешно сгенерирован ИИ из независимых кадров!"
        
    else:
        # ФОТО СҰРАЛҒАНДА: Бір ерекше сапалы сурет құрастырады
        seed = random.randint(1, 999999)
        img_url = f"https://image.pollinations.ai/p/{encoded_topic}_masterpiece?width=800&height=600&seed={seed}&nofeed=true&t={timestamp}"
        
        photo_html = f"""
        <div style="width:100%; max-width:800px; border-radius:12px; border:3px solid #10a37f; overflow:hidden; box-shadow:0 8px 24px rgba(0,0,0,0.1); margin:auto;">
            <img src="{img_url}" style="width:100%; height:auto; display:block;">
        </div>
        """
        st.markdown(photo_html, unsafe_allow_html=True)
        text_resp = f"Изображение по вашему запросу '{topic}' успешно создано автономным движком нейросети!"

    # 4. ОЗВУЧКА: Медиа толық шыққан БОЙДА ғана бот автоматты түрде сөйлейді
    st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
    
    return text_resp

# ВВОД СТРОКИ (INPUT)
if prompt := st.chat_input("Напишите запрос (например: фото приоры или видео робота)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = main_engine(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
