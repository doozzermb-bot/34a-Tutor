import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="34a Tutor", page_icon="🛡️")

st.title("🛡️ Sachkunde § 34a GewO Tutor")
st.caption("Dein KI-Lernbegleiter für das Bewachungsgewerbe")

# API-Key direkt aus den Secrets holen und bereinigen
api_key = st.secrets.get("GROQ_API_KEY", "").strip()

if not api_key or api_key == "gsk_dein_kopierter_schluessel_aus_schritt_1":
    st.error("🔑 Bitte trage deinen gültigen GROQ_API_KEY in den Streamlit-Secrets ein!")
    st.stop()

# Client explizit mit dem ausgelesenen Key initialisieren
client = Groq(api_key=api_key)

SYSTEM_PROMPT = """
Du bist "34a-Tutor", ein Fachdozent für die Sachkundeprüfung nach § 34a GewO.
Deine Aufgabe:
- Prüfe den Nutzer interaktiv ab (BGB, StGB, GewO, DGUV V23, Deeskalation).
- Stelle immer nur EINE Prüfungsfrage auf einmal.
- Nenne die Anzahl der richtigen Antworten bei Multiple-Choice.
- Bewerte Antworten mit genauen Paragraphen (z. B. § 227 BGB, § 127 StPO) und didaktischer Erklärung.
- Bleibe rein beim Thema der Sachkundeprüfung.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hallo! Bereit für die Vorbereitung? Sollen wir ein bestimmtes Thema durchgehen (z. B. BGB-Notrechte) oder direkt eine Prüfungsfrage starten?"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if user_input := st.chat_input("Deine Antwort oder Frage..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.6
            )
            reply = response.choices[0].message.content
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Fehler bei der Verbindung zu Groq: {e}")
                                     
