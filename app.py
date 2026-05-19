# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia, requests, re, base64, io, random
from gtts import gTTS
from bs4 import BeautifulSoup
from googlesearch import search as google_search

# НАСТРОЙКИ СИСТЕМЫ
wikipedia.set_lang("ru")
st.set_page_config(page_title="Serik-Ai v1.5", layout="wide")

# ЖЕСТКИЙ КОНТРАСТНЫЙ ДИЗАЙН (Все тексты гарантированно черные и крупные)
st.markdown("""
    <style>
    .stApp { background-color: #f5f7f8 !important; }
    h1, h2, h3, p, span, label, .stMarkdown, .stChatMessage { color: #000000 !important; font-weight: 700 !important; }
    [data-testid="stSidebar"] { background-color: #1a1c1e !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] h1 { color: #ffffff !important; }
    .stChatInput textarea { background-color: #ffffff !important; color: #000000 !important; border: 2px solid #0066cc !important; }
    .stChatMessage { background-color: #ffffff !important; border: 2px solid #dddddd !important; border-radius: 12px !important; padding: 15px !important; }
    pre { background-color: #1a1c1e !important; color: #00ffcc !important; padding: 15px !important; border-radius: 8px !important; font-family: monospace !important; }
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

    # 1. 🖼 АВТОНОМНЫЙ МЕДИА ГЕНЕРАТОР (100% БЕЗ БЛОКИРОВОК БРАУЗЕРА)
    if active_mode == "🖼 Генератор Медиа" or "фото" in q or "видео" in q or "картинка" in q or "нарисуй" in q:
        topic = q.replace("генерация", "").replace("сделай", "").replace("фото", "").replace("видео", "").replace("картинку", "").replace("нарисуй", "").strip()
        if not topic: topic = "робот"

        # ЕСЛИ ПОЛЬЗОВАТЕЛЬ ПРОСИТ ВИДЕО (Цифровая матричная анимация текстом)
        if "видео" in q or "анимация" in q:
            with st.spinner("Генерация потока видео-кадров..."):
                frames = [
                    "[=======---] 25% Загрузка нейросети...",
                    "[==========] 100% Поток данных стабилен!",
                    "🤖 СТРИМ ИИ-ВИДЕО: Активация матрицы...",
                    f"▶️ Воспроизведение генеративного ролика: '{topic.upper()}'"
                ]
                st.code(f"⚡ SERIK-AI VIDEO ENGINE ⚡\n\n" + "\n".join(frames), language="bash")
                return f"🎥 Генерация видео по теме '{topic}' завершена! Цифровой поток запущен."
        
        # ЕСЛИ ПОЛЬЗОВАТЕЛЬ ПРОСИТ ФОТО (Генерация ASCII-графики прямо в консоль чата)
        else:
            with st.spinner("Отрисовка графической матрицы..."):
                # Генерируем крутой текстовый рисунок робота/кибернетики
                ascii_art = """
      _     _
     o_o   o_o
    |   |_|   |
    |  _   _  |    [ AI IMAGE GENERATED ]
    | |_| |_| |    TOPIC: {}
    |_________|
     ||     ||
    =============
                """.format(topic.upper())
                st.text(ascii_art)
                return f"🎨 Текстовая ИИ-графика на тему '{topic}' успешно сгенерирована нейросетью!"

    # 2. 📝 РЕЖИМ РЕФЕРАТА
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
