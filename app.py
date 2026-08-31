import os
import streamlit as st
import requests

st.title("🛡️ 34a-Tutor Diagnosetest")

# Key aus Secrets laden
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ KEIN API-KEY GEFUNDEN! Bitte trage 'GROQ_API_KEY' in den Streamlit Secrets ein.")
else:
    st.success(f"✅ Key gefunden (beginnt mit: {api_key[:7]}...)")
    
    if st.button("Test-Anfrage an Groq senden"):
        with st.spinner("Verbindung wird getestet..."):
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": "Hallo"}]
                }
            )
            
            if res.status_code == 200:
                st.balloons()
                st.success("🎉 ERFOLG! Groq hat geantwortet:")
                st.write(res.json()["choices"][0]["message"]["content"])
            else:
                st.error(f"❌ Fehler Code {res.status_code}:")
                st.json(res.json())
                
