# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import re
import base64
from gtts import gTTS
import io

# Бет баптаулары
st.set_page_config(page_title="Serik-Ai AI Edition", layout="wide")
wikipedia.set_lang("ru")

# Дизайн
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stMarkdown, p, h1, h2, h3, span { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

def get_audio_html(text):
    try:
        clean_txt = re.sub(r'[^\w\sа-яА-ЯёЁ]', '', text)[:150]
        tts = gTTS(text=clean_txt, lang='ru')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_b64 = base64.b64encode(fp.read()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_b64}">'
    except: return ""

# Автоматты қате түзету функциясы (Түзеткіш)
def auto_correct(text):
    text = text.lower().strip()
    # Жиі кездесетін қателерді автоматты түзету
    corrections = {
        "рефератт": "реферат",
        "ессе": "эссе",
        "истария": "история",
        "расказ": "рассказ",
        "првет": "привет",
        "сссрр": "ссср",
        "казахстанн": "казахстан"
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Привет! Я Serik-Ai. Теперь я умею исправлять твои ошибки и составлять умные тексты сам. О чем напишем сегодня?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    st.markdown(get_audio_html(welcome), unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def ai_content_creator(q):
    q = auto_correct(q) # Сенің қатеңді түзетеді
    
    # Тез жауаптар
    brain = {
        "привет": "Привет! Я на связи. Исправлю любые ошибки и напишу лучший текст!",
        "как дела": "Все отлично, мой интеллект растет с каждым твоим вопросом.",
        "кто ты": "Я Serik-Ai, созданный Нуриком для генерации самых крутых текстов."
    }
    if q in brain: return brain[q]

    # Тақырыпты анықтау
    mode = "стандарт"
    if "реферат" in q: mode = "реферат"
    elif "эссе" in q: mode = "эссе"
    elif "история" in q or "рассказ" in q: mode = "история"

    topic = q.replace("напиши", "").replace("реферат", "").replace("эссе", "").replace("про", "").replace("рассказ", "").replace("историю", "").strip()

    try:
        # Wikipedia-дан мәтін алу
        search_results = wikipedia.search(topic)
        if not search_results:
            return f"Я понял, что ты имеешь в виду '{topic}', но даже в моей базе данных пока мало информации. Давай попробуем другую тему?"
        
        page = wikipedia.page(search_results[0])
        raw_text = page.content.split('. ')
        
        # Сөйлемдерді ақылды байланыстырушы сөздер
        connectors = ["Кроме того, ", "Важно отметить, что ", "Следовательно, ", "Более того, ", "Интересно, что "]
        
        smart_sentences = []
        for i, s in enumerate(raw_text[:60]): # 60 сөйлемге дейін жинау
            if len(s) > 30:
                # Әр 3-ші сөйлемге байланыстырушы сөз қосу (өздігінен құрастыру)
                if i % 3 == 0 and i != 0:
                    smart_sentences.append(connectors[i % len(connectors)] + s.lower())
                else:
                    smart_sentences.append(s)

        if mode == "реферат":
            res = f"### ИНТЕЛЛЕКТУАЛЬНЫЙ РЕФЕРАТ: {topic.upper()}\n\n"
            res += f"**Введение:** {page.summary[:500]}...\n\n"
            res += "**Основная часть:** " + ". ".join(smart_sentences[5:50]) + ".\n\n"
            res += "**Заключение:** Таким образом, анализ темы показывает, что " + smart_sentences[-1] + "."
            return res
        
        elif mode == "эссе":
            return f"### ЭССЕ: {topic.upper()}\n\nНа мой взгляд, данная тема заслуживает особого внимания. " + ". ".join(smart_sentences[:30]) + "."
        
        elif mode == "история":
            return f"### ИСТОРИЯ: {topic.upper()}\n\nВсе началось с того, что " + ". ".join(smart_sentences[:25]) + "."
            
        else:
            return ". ".join(smart_sentences[:15]) + "."

    except:
        return f"Я заметил ошибку в запросе или данных, но не волнуйся, я подстроил поиск под '{topic}'. К сожалению, именно сейчас база данных недоступна, попробуй еще раз!"

# Енгізу
if prompt := st.chat_input("Напиши рефератт про Сссрр..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Исправляю ошибки и создаю текст..."):
            response = ai_content_creator(prompt)
            st.markdown(response)
            st.markdown(get_audio_html(response), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
