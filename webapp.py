import streamlit as st
import csv
import os
import streamlit.components.v1 as components

# Configuração do arquivo CSV
def init_csv():
    if not os.path.exists("usuarios.csv"):
        with open("usuarios.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["usuario", "senha"])

# Registrar usuário
def registrar_usuario(usuario, senha):
    with open("usuarios.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([usuario, senha])
    return True

# Verificar login
def verificar_login(usuario, senha):
    with open("usuarios.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row == [usuario, senha]:
                return True
    return False

# Inicializar CSV
init_csv()

# Interface do usuário
st.sidebar.title("Login")
modo = st.sidebar.radio("Selecione uma opção", ["Login", "Registrar"])

usuario = st.sidebar.text_input("Usuário")
senha = st.sidebar.text_input("Senha", type="password")

if modo == "Registrar":
    if st.sidebar.button("Registrar"):
        registrar_usuario(usuario, senha)
        st.sidebar.success("Usuário registrado com sucesso! Agora faça login.")
else:
    if st.sidebar.button("Login"):
        if verificar_login(usuario, senha):
            st.session_state.autenticado = True
        else:
            st.sidebar.error("Credenciais incorretas")

# Verificar autenticação
if st.session_state.get("autenticado", False):
    tabs = st.tabs(["Rota Verde", "Loja Online"])
    
    with tabs[0]:
        st.title("🌳 Percurso de ciclovia Verde")
        mapa_html = '<iframe src="https://www.google.com/maps/d/embed?mid=1s7LuP4dZ2KLXqn481JQs2S2C_jCrZsw" width="100%" height="500"></iframe>'
        components.html(mapa_html, height=550)
    
    with tabs[1]:
        st.title("Loja Sustentável")
        produtos = [
            {"nome": "Cesta Orgânica", "preco": 12.99, "img": "Horta.png"},
            {"nome": "Sabonete Natural", "preco": 7.50, "img": "soap.png"},
            {"nome": "Bolsa Ecológica", "preco": 15.00, "img": "BolsaCometico.png"}
        ]
        
        if "carrinho" not in st.session_state:
            st.session_state.carrinho = []
        
        cols = st.columns(3)
        for idx, produto in enumerate(produtos):
            with cols[idx % 3]:
                st.image(produto['img'], width=200)
                st.write(f"**{produto['nome']}** - €{produto['preco']:.2f}")
                if st.button(f"Adicionar {produto['nome']}", key=produto['nome']):
                    st.session_state.carrinho.append(produto)
                    st.success(f"{produto['nome']} adicionado ao carrinho!")
        
        if st.session_state.carrinho:
            st.subheader("O Seu Carrinho")
            total = sum(item['preco'] for item in st.session_state.carrinho)
            for item in st.session_state.carrinho:
                st.write(f"{item['nome']} - €{item['preco']:.2f}")
            st.write(f"**Total: €{total:.2f}**")
