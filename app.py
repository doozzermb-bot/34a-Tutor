import os
import streamlit as st
import requests

st.set_page_config(page_title="34a Tutor", page_icon="🛡️")

st.title("🛡️ Sachkunde § 34a GewO Tutor")
st.caption("Dein KI-Lernbegleiter für das Bewachungsgewerbe")

api_key = st.secrets.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """
Du bist „34a-Tutor“, ein Fachdozent für die Sachkundeprüfung nach § 34a GewO.
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

if prompt := st.chat_input("Deine Antwort oder Frage..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": st.session_state.messages,
            }
        )
        data = response.json()
        
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)
        else:
            st.error(f"Fehler von OpenRouter: {data.get('error', {}).get('message', data)}")
            
    except Exception as e:
        st.error(f"Fehler bei der Verbindung: {e}")
        
