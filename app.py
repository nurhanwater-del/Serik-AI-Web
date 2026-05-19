# -*- coding: utf-8 -*-
import streamlit as st
import requests, re, base64, io, random
from gtts import gTTS
from requests.utils import quote

# НАСТРОЙКИ СИСТЕМЫ (Стиль ChatGPT - Светлый, чистый и понятный)
st.set_page_config(page_title="Serik-Ai v2.5 | Knowledge & Photo Engine", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f7f7f8 !important; }
    h1, h2, h3, p, span, label, .stMarkdown, .stChatMessage { color: #1f1f1f !important; font-weight: 500 !important; }
    [data-testid="stSidebar"] { background-color: #202123 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] h1 { color: #ffffff !important; }
    .stChatInput textarea { background-color: #ffffff !important; color: #000000 !important; border: 1px solid #e5e5e5 !important; border-radius: 8px !important; }
    .stChatMessage { background-color: #ffffff !important; border: 1px solid #e5e5e5 !important; border-radius: 8px !important; padding: 15px !important; margin-bottom: 10px !important; }
    
    .photo-container {
        width: 100%;
        max-width: 700px;
        border-radius: 8px;
        border: 1px solid #e5e5e5;
        overflow: hidden;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 🔊 ФУНКЦИЯ ОЗВУЧКИ
def get_voice_player(text):
    try:
        clean = re.sub(r'[^\w\s]', '', text[:250])
        tts = gTTS(text=clean, lang='ru')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
    except: return ""

# БОКОВАЯ ПАНЕЛЬ
with st.sidebar:
    st.title("💠 Serik-Ai v2.5")
    st.write("---")
    st.success("📚 Текст, Рефераты и Фото-генератор")
    st.write("---")
    st.info("Разработчик: Нурик")
    if st.button("Сбросить диалог"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# ИНТЕРНЕТТЕН МӘТІН ОҚЫП, АҚПАРАТ ІЗДЕУ ФУНКЦИЯСЫ (Википедия арқылы)
def search_internet_info(topic):
    try:
        url = f"https://ru.wikipedia.org/api/rest_v1/page/summary/{quote(topic)}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "")
    except: pass
    return ""

# --- БАСТЫ ИИ-ДВИЖОК ---
def main_engine(query):
    q = query.strip()
    q_low = q.lower()

    # 👤 АВТОР ТУРАЛЫ СҰРАҚҚА ЖАУАП
    if "кто тебя создал" in q_low or "кто твой автор" in q_low or "сені кім жасады" in q_low or "автор" in q_low:
        text_resp = "Меня создал Нурик! Я — официальный ИИ Серік-Ай, обученный писать эссе, рефераты и искать информацию."
        st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
        return text_resp

    # ФОТО ГЕНЕРАТОР (Егер сұраныста фото немесе картинка сөзі болса)
    if "фото" in q_low or "картинка" in q_low or "нарисуй" in q_low or "рисунок" in q_low:
        clean_prompt = q_low.replace("фото", "").replace("картинку", "").replace("нарисуй", "").replace("рисунок", "").replace("сделай", "").strip()
        if not clean_prompt: clean_prompt = "beautiful landscape"
        
        seed = random.randint(1, 999999)
        img_url = f"https://image.pollinations.ai/p/{quote(clean_prompt)}?width=800&height=600&seed={seed}&nofeed=true"
        
        photo_html = f"""
        <div class="photo-container">
            <img src="{img_url}" style="width:100%; height:auto; display:block;">
        </div>
        """
        st.markdown(photo_html, unsafe_allow_html=True)
        text_resp = f"Изображение по вашему запросу '{clean_prompt}' успешно сгенерировано."
        st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
        return text_resp

    # МӘТІН, ЭССЕ, РЕФЕРАТ, ӘҢГІМЕ ҚҰРАСТЫРУ БӨЛІМІ
    with st.spinner("ИИ изучает материалы в сети и пишет текст..."):
        # Сұраныстан артық сөздерді алып тастап, негізгі тақырыпты анықтаймыз
        search_topic = q.replace("реферат", "").replace("эссе", "").replace("рассказ", "").replace("история", "").replace("про", "").replace("на тему", "").strip()
        
        # Интернеттен мәлімет іздейміз
        web_info = search_internet_info(search_topic)
        
        # Оқыған ақпарат негізінде ИИ өз сөйлемдерін құрастырады
        if web_info:
            if "эссе" in q_low:
                text_resp = f"### Эссе на тему: {search_topic}\n\n**Введение:** {search_topic} является важным понятием в истории и культуре. На основе изученных данных, {web_info[:150]}...\n\n**Основная часть:** Рассматривая этот вопрос глубже, стоит отметить, что исследования подтверждают ключевые факты: {web_info}. Этот процесс открывает новые взгляды на события.\n\n**Заключение:** Таким образом, анализ темы показывает её глубокое влияние на современность."
            elif "реферат" in q_low:
                text_resp = f"### Реферат: {search_topic}\n\n**1. Введение**\nДанная работа посвящена изучению темы '{search_topic}'. Актуальность исследования обусловлена развитием научных взглядов.\n\n**2. Основное содержание**\nПо данным открытых источников: {web_info}\n\n**3. Заключение**\nВ ходе сбора материала были изучены ключевые аспекты и структурированы основные выводы по теме."
            else:
                text_resp = f"### История / Рассказ: {search_topic}\n\nВот что удалось собрать и проанализировать по вашему запросу:\n\n{web_info}\n\nЕсли вам нужно развернуть отдельный пункт в виде полноценного реферата, просто укажите это."
        else:
            # Егер интернеттен нақты мақала табылмаса, ИИ базалық білімімен сөйлем құрайды
            text_resp = f"Я проанализировал запрос '{q}'. На основе общей базы знаний ИИ: это понятие имеет широкое значение. Для составления точного исторического реферата или эссе, пожалуйста, уточните конкретные детали или имена."

    # Жауап дайын болғанда бірден дыбыстау
    st.markdown(get_voice_player(text_resp), unsafe_allow_html=True)
    return text_resp

# ВВОД СТРОКИ
if prompt := st.chat_input("Напишите тему для эссе/реферата или запрос для фото..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = main_engine(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
