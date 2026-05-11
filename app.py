# -*- coding: utf-8 -*-
import streamlit as st
import wikipedia
import re
import base64
from gtts import gTTS
import io

# Настройка
st.set_page_config(page_title="Serik-Ai Fixed", layout="wide")
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

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Привет! Я Serik-Ai. Теперь я лучше понимаю вопросы и не путаю города. О чем напишем?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    st.markdown(get_audio_html(welcome), unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generate_fixed_text(q):
    q = q.lower().strip()
    
    # 1. СӘЛЕМДЕСУ ЖӘНЕ ТАНЫСТЫРУ (Бұл енді 100% істейді)
    if any(x in q for x in ["привет", "салам", "здравствуй"]):
        return "Привет! Я твой верный помощник Serik-Ai v1.0. Готов написать реферат, эссе или историю. Просто дай мне тему!"
    
    if any(x in q for x in ["кто ты", "как тебя зовут"]):
        return "Я — Serik-Ai, мощный искусственный интеллект, созданный Нұриком для помощи в учебе и написания крутых текстов."

    if "как дела" in q:
        return "У меня все отлично! Мои алгоритмы настроены на максимум. Какую тему сегодня разберем?"

    # 2. СӨЗ САНЫН АНЫҚТАУ
    word_count_match = re.search(r'(\d+)\s*(слов|слово|слова)', q)
    target_words = int(word_count_match.group(1)) if word_count_match else 500

    # Тақырыпты тазалау
    topic = re.sub(r'(\d+)\s*(слов|слово|слова)', '', q)
    topic = topic.replace("напиши", "").replace("реферат", "").replace("эссе", "").replace("про", "").replace("рассказ", "").strip()

    try:
        # 3. НАҚТЫ ІЗДЕУ (Ақтөбені Ресеймен шатастырмау үшін)
        search_results = wikipedia.search(topic)
        if not search_results:
            return f"Я не смог найти точную информацию про '{topic}'. Попробуй уточнить запрос, например: 'город Актобе'."
        
        # Ең жақын нәтижені алу
        page = wikipedia.page(search_results[0])
        
        # Егер сұрақ Ақтөбе туралы болса, тек Қазақстанға қатысты мәтінді алу
        raw_content = page.content
        if "актобе" in topic:
            # Ресей туралы бөлімдерді алып тастауға тырысу
            raw_content = re.sub(r'Россия.*?\n', '', raw_content)

        raw_sentences = raw_content.split('. ')
        connectors = ["Важно отметить, что ", "Кроме того, ", "Интересно, что ", "Следовательно, ", "Также стоит добавить, что "]
        
        final_text_list = []
        current_words = 0
        
        while current_words < target_words and len(final_text_list) < 300:
            for i, s in enumerate(raw_sentences):
                if current_words >= target_words: break
                if len(s) > 30:
                    prefix = connectors[i % len(connectors)] if i % 4 == 0 else ""
                    new_s = prefix + s.strip() + ". "
                    final_text_list.append(new_s)
                    current_words += len(new_s.split())
            if current_words < target_words: # Мәтін жетпесе, аздап қайталау немесе кеңейту
                raw_sentences = [s + " (подробности в контексте)" for s in raw_sentences]

        final_text = "".join(final_text_list)
        
        header = f"### {topic.upper()}\n\n"
        if "реферат" in q: header = f"### РЕФЕРАТ: {topic.upper()} (Цель: {target_words} слов)\n\n"
        elif "эссе" in q: header = f"### ЭССЕ: {topic.upper()}\n\n"

        return header + final_text

    except:
        return f"По теме '{topic}' произошла ошибка. Попробуй написать запрос по-другому, например: 'Актобе Казахстан'."

# Input
if prompt := st.chat_input("Напиши про Актобе на 300 слов..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Анализирую и пишу..."):
            response = generate_fixed_text(prompt)
            st.markdown(response)
            st.caption(f"📊 Всего слов: {len(response.split())}")
            st.markdown(get_audio_html(response), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
