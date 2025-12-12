import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Configuração inicial
load_dotenv()
st.set_page_config(page_title="Chatbot Gemini", page_icon="🤖")
st.title("🤖 Meu Primeiro Chatbot com IA")

# Configuração da API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Configure sua chave API no arquivo .env")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Histórico de conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Gera e exibe a resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
