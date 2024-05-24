import streamlit as st
import ldap3
from ldap3.core.exceptions import LDAPBindError

# Função para autenticar usuário no LDAP
def authenticate_user(username, password):
    server = ldap3.Server('ldap://your_ldap_server')
    conn = ldap3.Connection(server, user=f"your_domain\\{username}", password=password)
    try:
        if conn.bind():
            return True
    except LDAPBindError:
        return False
    finally:
        conn.unbind()
    return False

# Função principal para a interface do Streamlit
def main():
    st.title('Interface de Autenticação')

    st.sidebar.header('Login')
    username = st.sidebar.text_input('Usuário')
    password = st.sidebar.text_input('Senha', type='password')

    if st.sidebar.button('Login'):
        if authenticate_user(username, password):
            st.success('Login bem-sucedido!')
            # Lógica para mostrar o dashboard após o login bem-sucedido
            show_dashboard()
        else:
            st.error('Usuário ou senha incorretos.')

# Função para exibir o dashboard após autenticação
def show_dashboard():
    st.header('Dashboard')
    # Adicione aqui os elementos do seu dashboard
    st.write('Bem-vindo ao Dashboard!')

if __name__ == '__main__':
    main()


