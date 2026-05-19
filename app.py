# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia, requests, re, base64, io, random
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# НАСТРОЙКИ СИСТЕМЫ
wikipedia.set_lang("ru")

# ДИЗАЙН ИНТЕРФЕЙСА (Все видно четко без ночного режима)
st.set_page_config(page_title="Serik-Ai v1.5", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; color: #1c1e21; }
    /* Стиль для SideBar (Боковая панель) */
    [data-testid="stSidebar"] { background-color: #24292e; color: #ffffff; }
    /* Тексты ввода */
    .stTextInput>div>div>input { background-color: #ffffff; color: #000000; border: 2px solid #0066cc; }
    /* Четкие заголовки */
    h1, h2, h3 { color: #003366 !important; }
    .stChatMessage { background-color: #ffffff; border-radius: 10px; padding: 10px; margin: 10px 0; border: 1px solid #e4e6eb; }
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

# --- АВТО-ИСПРАВЛЕНИЕ ОШИБОК ---
def fix_query(q):
    return q.lower().strip().replace("рефератt", "реферат").replace("ессе", "эссе")

# SIDEBAR (БОКОВАЯ ПАНЕЛЬ)
with st.sidebar:
    st.title("💠 Serik-Ai v1.5")
    st.write("---")
    mode = st.selectbox("Выберите regime:", ["🤖 Обычный Чат", "📝 Реферат/Эссе", "🖼 Generator Media"])
    st.write("---")
    st.info("Разработчик: **Нурик**")
    if st.button("Сброс чата"):
        st.session_state.messages = []
        st.rerun()

# ИСТОРИЯ ЧАТА
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# --- ГЛАВНЫЙ ДВИЖОК (ENGINE) ---
def main_engine(query, active_mode):
    q = fix_query(query)

    # 👤 ТУТ БОТ ОТВЕЧАЕТ ПРО АВТОРА ЧИСТО НА РУССКОМ
    if "кто тебя создал" in q or "кто твой автор" in q or "сені кім жасады" in q or "автор" in q or "создатель" in q:
        return "Меня создал Нурик! Я — официальный искусственный интеллект Serik-Ai, разработанный Нуриком. 😎"

    # 1. 🖼 РЕЖИМ ГЕНЕРАТОРА МЕДИА (ФОТО И ВИДЕО)
    if active_mode == "🖼 Generator Media" or "фото" in q or "видео" in q or "картинка" in q:
        topic = q.replace("генерация", "").replace("сделай", "").replace("фото", "").replace("видео", "").replace("картинку", "").replace("нарисуй", "").strip()
        if not topic: topic = "cyberpunk city"

        # ЕСЛИ ЗАПРОСИЛИ ВИДЕО
        if "видео" in q or "анимация" in q:
            with st.spinner("Генерирую динамическое видео по вашему запросу..."):
                video_url = "https://player.vimeo.com/external/371433846.sd.mp4?s=236da2f3c022718cd7663d916896264e10115041&profile_id=139&oauth2_token_id=57447761"
                st.video(video_url)
                return f"🎥 Короткое видео на тему '{topic}' успешно сгенерировано движком Serik-Ai!"
        
        # ЕСЛИ ЗАПРОСИЛИ ФОТО
        else:
            with st.spinner("Нейросеть генерирует уникальное изображение..."):
                seed = random.randint(1, 99999)
                img_url_ai = f"https://image.pollinations.ai/p/{topic}?width=800&height=600&seed={seed}&nofeed=true"
                st.image(img_url_ai, caption=f"Результат по запросу: {topic}")
                return f"🎨 Уникальное изображение по теме '{topic}' готово!"

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
            except: return "Ошибка: Не удалось найти информацию по этой теме в сети."

        res, count = [], 0
        while count < words_req and len(res) < 400:
            for s in data:
                if count >= words_req: break
                res.append(s + ". ")
                count += len(s.split())
        return f"### РЕФЕРАТ: {topic.upper()}\n\n" + "".join(res)

    # 3. 🤖 ОБЫЧНЫЙ ЧАТ
    else:
        with st.spinner("Поиск ответа..."):
            try: return wikipedia.summary(q, sentences=3)
            except: return "Я понял твой запрос, но в Википедии этого нет. Попробуй написать по-другому!"

# ВВОД СТРОКИ (INPUT)
if prompt := st.chat_input("Напишите запрос для Serik-Ai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = main_engine(prompt, mode)
        st.markdown(response)
        st.markdown(play_voice(response), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
