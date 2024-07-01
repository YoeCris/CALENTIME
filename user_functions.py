# user_functions.py

import streamlit as st
import pandas as pd
from user_management import UserManagement

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()

# Función para verificar el estado de un documento (simulado)
def check_document_status(doc_id):
    return f"Estado del documento {doc_id}: Pendiente"

# Función para manejar el inicio de sesión
def login(username, password):
    user = user_management.get_user_by_username(username)
    if user and user['password'] == password:
        st.session_state.authenticated = True
        st.session_state.role = user['role']
        st.session_state.username = username
        st.session_state.password_attempts = 3
        return True
    else:
        st.warning("Nombre de usuario o contraseña inválidos")
        return False

def user_interface():
    st.sidebar.subheader("Iniciar Sesión")
    
    with st.sidebar.form("login_form"):
        username = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type='password')
        login_button = st.form_submit_button("Iniciar Sesión")
        
        if login_button:
            login(username, password)
    
    if st.session_state.authenticated:
        st.sidebar.subheader("Menú de Usuario")
        choice = st.sidebar.radio("Seleccione una opción:", ["Ver Documentos", "Administrar Mi Usuario", "Cerrar Sesión"])
        
        if choice == "Cerrar Sesión":
            st.session_state.authenticated = False
            st.session_state.role = None
            st.session_state.username = None
            st.experimental_rerun()

        elif choice == "Ver Documentos":
            st.subheader("Ver Documentos")
            casos = user_management.get_cases_by_reviewer(st.session_state.username)
    
            if casos:
                df = pd.DataFrame(casos)
                df.columns = ['id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'stage']
                df = df.rename(columns={
                    'id': 'ID',
                    'code': 'Código del Documento',
                    'investigated_last_name': 'Apellidos del Investigado',
                    'investigated_first_name': 'Nombre del Investigado',
                    'dni': 'DNI del Investigado',
                    'reviewer': 'Encargado de Revisar el Documento',
                    'stage': 'Etapa',
                })
                st.dataframe(df)
            else:
                st.warning("No hay documentos disponibles para mostrar.")

        elif choice == "Administrar Mi Usuario":
            st.subheader("Administrar Mi Usuario")
            # Aquí se puede agregar código adicional para que los usuarios administren su propia información, como cambiar la contraseña, etc.
