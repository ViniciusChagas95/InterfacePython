import streamlit as st
import oracledb

# Função para verificar usuário no banco de dados Oracle
def authenticate_user_db(username, password):
    try:
        # Conecte-se ao banco de dados Oracle
        dsn = oracledb.makedsn('oracle.fiap.com.br', 1521, service_name='orcl')
        conn = oracledb.connect(user='rm550167', password='051095', dsn=dsn)
        cursor = conn.cursor()
        
        # Execute a consulta para verificar as credenciais
        cursor.execute("SELECT COUNT(*) FROM USERS WHERE username=:username AND password=:password", 
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
        if authenticate_user_db(username, password):
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
