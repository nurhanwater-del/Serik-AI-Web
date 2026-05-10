# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import re
import base64
from gtts import gTTS
import io

# Бет баптаулары
st.set_page_config(page_title="Serik-Ai Custom Words", layout="wide")
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

# Авто-түзету
def auto_correct(text):
    text = text.lower().strip()
    corrections = {"рефератт": "реферат", "ессе": "эссе", "истария": "история", "расказ": "рассказ"}
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Привет! Теперь я могу писать тексты ровно на столько слов, сколько ты попросишь. Просто напиши: 'Реферат про космос на 500 слов'."
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    st.markdown(get_audio_html(welcome), unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generate_custom_text(q):
    q = auto_correct(q)
    
    # Сөз санын анықтау (мысалы: "на 500 слов")
    word_count_match = re.search(r'(\d+)\s*(слов|слово|слова)', q)
    if word_count_match:
        target_words = int(word_count_match.group(1))
    else:
        target_words = 500 # Егер айтпаса, стандартты 500 сөз

    topic = re.sub(r'(\d+)\s*(слов|слово|слова)', '', q)
    topic = topic.replace("напиши", "").replace("реферат", "").replace("эссе", "").replace("про", "").strip()

    try:
        search_results = wikipedia.search(topic)
        if not search_results:
            return f"Я понял, что ты хочешь текст на {target_words} слов про '{topic}', но информации маловато. Попробуй другую тему."
        
        page = wikipedia.page(search_results[0])
        # Мәтінді сөйлемдерге бөлу
        raw_sentences = page.content.split('. ')
        
        # Сөйлемдерді байланыстырушы сөздермен байыту
        connectors = ["Кроме того, ", "Важно отметить, что ", "Следовательно, ", "Более того, ", "Интересно, что "]
        
        final_text_list = []
        current_word_count = 0
        
        # Мәтінді керекті сөз санына жеткенше жинау
        while current_word_count < target_words and len(final_text_list) < 200:
            for i, s in enumerate(raw_sentences):
                if current_word_count >= target_words:
                    break
                if len(s) > 20:
                    prefix = connectors[i % len(connectors)] if i % 3 == 0 else ""
                    new_sentence = prefix + s.strip() + ". "
                    final_text_list.append(new_sentence)
                    current_word_count += len(new_sentence.split())
            # Егер мәтін жетпесе, айналымды қайталау (созу үшін)
            if current_word_count < target_words:
                raw_sentences = [s + " (подробности далее)" for s in raw_sentences]

        final_text = "".join(final_text_list)
        
        # Форматтау
        if "реферат" in q:
            return f"### РЕФЕРАТ: {topic.upper()} (Приблизительно {target_words} слов)\n\n" + final_text
        elif "эссе" in q:
            return f"### ЭССЕ: {topic.upper()}\n\n" + final_text
        else:
            return f"### ИСТОРИЯ: {topic.upper()}\n\n" + final_text

    except:
        return "Произошла ошибка. Попробуй еще раз, уточнив название темы!"

# Input
if prompt := st.chat_input("Напиши реферат про СССР на 1000 слов..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Генерирую текст..."):
            response = generate_custom_text(prompt)
            st.markdown(response)
            # Сөз санын есептеп көрсету
            real_count = len(response.split())
            st.caption(f"📊 Всего слов: {real_count}")
            st.markdown(get_audio_html(response), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
