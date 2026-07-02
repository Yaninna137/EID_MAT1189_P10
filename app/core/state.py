import streamlit as st

def inicializar_session_state():
    if 'modelo' not in st.session_state:
        st.session_state.modelo = None
 