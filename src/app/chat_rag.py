import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.rag_answer import responder_pergunta

import streamlit as st

st.set_page_config(page_title="Chat CIMT", page_icon="💬")
st.title("💬 Assistente CIMT")
st.caption("Pergunte algo sobre o conteúdo das aulas do curso CIMT.")

if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

for msg in st.session_state["mensagens"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

pergunta = st.chat_input("Digite sua pergunta sobre a CIMT...")

if pergunta:
    st.session_state["mensagens"].append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando os documentos..."):
            resposta = responder_pergunta(pergunta)
            st.markdown(resposta)
            st.session_state["mensagens"].append({"role": "assistant", "content": resposta})
