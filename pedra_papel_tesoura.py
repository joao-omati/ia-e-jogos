import streamlit as st
import random

st.set_page_config(page_title="Pedra, Papel e Tesoura", page_icon="✊", layout="centered")

st.title("✊✋✌ Pedra, Papel ou Tesoura")
st.markdown("Desafie o computador nesse clássico jogo!")

# Sessão para armazenar estado
if "resultado" not in st.session_state:
    st.session_state.resultado = ""
if "jogando" not in st.session_state:
    st.session_state.jogando = True

# Função do jogo
def jogar(escolha_usuario):
    opcoes = ["Pedra", "Papel", "Tesoura"]
    escolha_pc = random.choice(opcoes)

    if escolha_usuario == escolha_pc:
        resultado = "🤝 Empate!"
    elif (escolha_usuario == "Pedra" and escolha_pc == "Tesoura") or \
         (escolha_usuario == "Papel" and escolha_pc == "Pedra") or \
         (escolha_usuario == "Tesoura" and escolha_pc == "Papel"):
        resultado = "🎉 Você venceu!"
    else:
        resultado = "💥 Você perdeu!"

    st.session_state.resultado = f"🧍 Você: **{escolha_usuario}**\n🖥️ Computador: **{escolha_pc}**\n\n**{resultado}**"
    st.session_state.jogando = False

# Interface de botões
if st.session_state.jogando:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✊ Pedra", use_container_width=True):
            jogar("Pedra")
    with col2:
        if st.button("✋ Papel", use_container_width=True):
            jogar("Papel")
    with col3:
        if st.button("✌ Tesoura", use_container_width=True):
            jogar("Tesoura")

# Resultado da partida
if not st.session_state.jogando:
    st.markdown("---")
    st.markdown(st.session_state.resultado)

    # Botão para jogar novamente
    if st.button("🔁 Jogar Novamente"):
        st.session_state.resultado = ""
        st.session_state.jogando = True
