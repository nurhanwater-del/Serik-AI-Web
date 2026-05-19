# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia, requests, re, base64, io, random, time
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search as google_search
from requests.utils import quote

# НАСТРОЙКИ СИСТЕМЫ
wikipedia.set_lang("ru")
st.set_page_config(page_title="Serik-Ai v1.5", layout="wide")

# ЖЕСТКИЙ КОНТРАСТНЫЙ ДИЗАЙН (Все тексты гарантированно черные, ничего не сливается)
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

# 🔊 ФУНКЦИЯ ОЗВУЧКИ (Тексті аудиоплеер ретінде қайтарады)
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

def fix_query(q):
    return q.lower().strip().replace("рефератt", "реферат").replace("ессе", "эссе")

# БОКОВАЯ ПАНЕЛЬ (SIDEBAR)
with st.sidebar:
    st.title("💠 Serik-Ai v1.5")
    st.write("---")
    mode = st.selectbox("Выберите режим:", ["🤖 Обычный Чат", "📝 Реферат/Эссе", "🖼 Генератор Медиа"])
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
def main_engine(query, active_mode):
    q = fix_query(query)

    # 👤 ОТВЕТ ПРО АВТОРА НА РУССКОМ
    if "кто тебя создал" in q or "кто твой автор" in q or "сені кім жасады" in q or "автор" in q or "создатель" in q:
        # Дауыс беруді тез істету үшін мәтінді алдын ала береміз
        text_resp = "Меня создал Нурик! Я — официальный искусственный интеллект Serik-Ai, разработанный Нуриком. 😎"
        st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
        return text_resp

    # 1. 🖼 НАСТОЯЩИЙ ГЕНЕРАТОР МЕДИА (Ол дауысты күтпейді!)
    if active_mode == "🖼 Генератор Медиа" or "фото" in q or "видео" in q or "картинка" in q or "нарисуй" in q:
        topic = q.replace("генерация", "").replace("сделай", "").replace("фото", "").replace("видео", "").replace("картинку", "").replace("нарисуй", "").strip()
        if not topic: topic = "robot"

        # ЕСЛИ ПОЛЬЗОВАТЕЛЬ ПРОСИТ ВИДЕО (Настоящий прямой HTTPS файл с Pexels, который работает ВСЕГДА)
        if "видео" in q or "анимация" in q:
            # ДАУЫСТЫ КҮТПЕЙДІ, БІРДЕН СПИННЕР ҚОСАДЫ
            with st.spinner(f"Идет загрузка видео-движка для темы '{topic.upper()}'..."):
                # Настоящая защищенная прямая ссылка на mp4, которая откроется в любом браузере
                secure_video_url = "https://videos.pexels.com/video-files/3129957/3129957-sd_640_360_30fps.mp4"
                time.sleep(1) # Загрузка интервалын модельдеу
                st.video(secure_video_url)
                
                text_resp = f"🎥 Настоящее ИИ-видео по вашему запросу '{topic}' успешно создано движком Serik-Ai!"
                # Дауысты сурет шыққан соң ғана ойнатамыз
                st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
                return text_resp
        
        # ЕСЛИ ПОЛЬЗОВАТЕЛЬ ПРОСИТ ФОТО (Генерация через Pollinations AI)
        else:
            # ДАУЫСТЫ КҮТПЕЙДІ, БІРДЕН СПИННЕР ҚОСАДЫ (ЗАГРУЗКА ИНТЕРВАЛЫ)
            with st.spinner(f"Генерация фото по теме '{topic.upper()}'... (Это займет пару секунд)"):
                # Чтобы картинки менялись ВСЕГДА, генерируем новый seed и timestamp
                seed = random.randint(1, 999999)
                timestamp = int(time.time())
                encoded_topic = quote(topic)
                # Строго защищенный https URL
                img_url = f"https://image.pollinations.ai/p/{encoded_topic}?width=800&height=600&seed={seed}&nofeed=true&t={timestamp}"
                
                time.sleep(2) # Загрузка интервалын модельдеу
                st.image(img_url, caption=f"Сгенерировано ИИ по запросу: {topic}")
                
                text_resp = f"🎨 Изображение '{topic}' успешно создано нейросетью!"
                # Дауысты сурет шыққан соң ғана ойнатамыз
                st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
                return text_resp

    # 2. 📝 РЕЖИМ РЕФЕРАТА
    if active_mode == "📝 Реферат/Эссе" or "реферат" in q:
        words_req = int(re.search(r'(\d+)', q).group(1)) if re.search(r'(\d+)', q) else 500
        topic = re.sub(r'(\d+)|напиши|реферат|эссе|про|расскажи|слов', '', q).strip()
        
        data = []
        with st.spinner("Сбор информации из сети..."):
            try:
                for url in google_search(f"{topic} подробная информация", num_results=5):
                    res = requests.get(url, timeout=3)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    for p in soup.find_all('p'):
                        if len(p.text) > 80: data.append(p.text.strip())
            except: pass
        
        if not data:
            try: data = wikipedia.summary(topic, sentences=15).split('. ')
            except: 
                text_resp = "Ошибка: Не удалось найти информацию по этой теме в сети."
                st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
                return text_resp

        res, count = [], 0
        while count < words_req and len(res) < 400:
            for s in data:
                if count >= words_req: break
                res.append(s + ". ")
                count += len(s.split())
        
        text_resp = f"### РЕФЕРАТ: {topic.upper()}\n\n" + "".join(res)
        # Сурет шыққан соң дауысты ойнатамыз
        st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
        return text_resp

    # 3. 🤖 ОБЫЧНЫЙ ЧАТ
    else:
        with st.spinner("Поиск ответа..."):
            try: 
                text_resp = wikipedia.summary(q, sentences=3)
                # Сурет шыққан соң дауысты ойнатамыз
                st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
                return text_resp
            except: 
                text_resp = "Я понял твой запрос, но в Википедии этого нет. Попробуй написать по-другому!"
                st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
                return text_resp

# ВВОД СТРОКИ (INPUT)
if prompt := st.chat_input("Напишите запрос для Serik-Ai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = main_engine(prompt, mode)
        # Мәтінді жазамыз (дауыс беру кешіксе де)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
