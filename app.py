import streamlit as st
import ldap3
import oracledb
from ldap3.core.exceptions import LDAPBindError

# Função para autenticar usuário no LDAP
def authenticate_user_ldap(username, password):
    server = ldap3.Server('ldap://your_ldap_server', port=389, use_ssl=False)
    conn = ldap3.Connection(server, user=f"your_domain\\{username}", password=password)
    try:
        if conn.bind():
            return True
    except LDAPBindError:
        return False
    finally:
        conn.unbind()
    return False

# Função para verificar usuário no banco de dados Oracle
def authenticate_user_db(username, password):
    try:
        # Conecte-se ao banco de dados Oracle
        dsn = oracledb.makedsn('db_host', 1521, service_name='db_service')
        conn = oracledb.connect(user='db_user', password='db_password', dsn=dsn)
        cursor = conn.cursor()
        
        # Execute a consulta para verificar as credenciais
        cursor.execute("SELECT COUNT(*) FROM users WHERE username=:username AND password=:password", 
                       username=username, password=password)
        result = cursor.fetchone()
        
        # Feche a conexão com o banco de dados
        cursor.close()
        conn.close()
        
        # Verifique se o usuário existe
        if result[0] == 1:
            return True
        else:
            return False
    except oracledb.DatabaseError as e:
        st.error(f"Erro de conexão com o banco de dados: {e}")
        return False

# Função principal para a interface do Streamlit
def main():
    st.title('Interface de Autenticação')

    st.sidebar.header('Login')
    username = st.sidebar.text_input('Usuário')
    password = st.sidebar.text_input('Senha', type='password')

    if st.sidebar.button('Login'):
        if authenticate_user_ldap(username, password) and authenticate_user_db(username, password):
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
