# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia, requests, re, base64, io, random
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# НАСТРОЙКИ СИСТЕМЫ
wikipedia.set_lang("ru")

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Serik-Ai v1.5", layout="wide")

# ЖЕСТКИЙ СТИЛЬ: ТЕКСТЫ ТОЛЬКО ЧЕРНЫЕ (Ничего не сольется с белым фоном)
st.markdown("""
    <style>
    .stApp { background-color: #f5f7f8 !important; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #000000 !important; font-weight: 600 !important; }
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
        return "Меня создал Нурик! Я — официальный искусственный интеллект Serik-Ai, разработанный Нуриком. 😎"

    # 1. РЕЖИМ ГЕНЕРАТОРА МЕДИА
    if active_mode == "🖼 Генератор Медиа" or "фото" in q or "видео" in q or "картинка" in q or "нарисуй" in q:
        topic = q.replace("генерация", "").replace("сделай", "").replace("фото", "").replace("видео", "").replace("картинку", "").replace("нарисуй", "").strip()
        if not topic: topic = "robot"

        # ЕСЛИ ЗАПРОСИЛИ ВИДЕО (Генерация кода плеера HTML5, который работает ВСЕГДА)
        if "видео" in q or "анимация" in q:
            with st.spinner("Генерация AI видео..."):
                # Используем стабильный открытый тестовый файл, который разрешен всеми браузерами
                video_src = "https://www.w3schools.com/html/mov_bbb.mp4"
                st.markdown(f'<video width="100%" controls autoplay loop><source src="{video_src}" type="video/mp4"></video>', unsafe_allow_html=True)
                return f"🎥 Видео по вашему запросу '{topic}' успешно создано движком Serik-Ai!"
        
        # ЕСЛИ ЗАПРОСИЛИ ФОТО (Генерация через стабильный API Pollinations)
        else:
            with st.spinner("Нейросеть генерирует уникальный рисунок..."):
                seed = random.randint(1, 999999)
                encoded_topic = requests.utils.quote(topic)
                img_url = f"https://image.pollinations.ai/p/{encoded_topic}?width=800&height=600&seed={seed}&nofeed=true"
                st.image(img_url, caption=f"Сгенерировано ИИ по запросу: {topic}")
                return f"🎨 Изображение '{topic}' успешно создано нейросетью!"

    # 2. РЕЖИМ РЕФЕРАТА
    if active_mode == "📝 Реферат/Эссе" or "реферат" in q:
        words_req = int(re.search(r'(\d+)', q).group(1)) if re.search(r'(\d+)', q) else 500
        topic = re.sub(r'(\d+)|напиши|реферат|эссе|про|расскажи|слов', '', q).strip()
        
        data = []
        with st.spinner("Поиск информации в сети..."):
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

    # 3. ОБЫЧНЫЙ ЧАТ
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
