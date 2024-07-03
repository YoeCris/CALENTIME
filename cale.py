import streamlit as st
from user_management import UserManagement
from user_functions import user_interface
from admin_functions import admin_interface

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()
user_management.create_default_superusers()

# Simular el estado de autenticación (puede ser mejorado con una solución más segura)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.password_attempts = 3

# Título de la aplicación
st.title("Sistema de Gestión de Casos")

def check_document_status(doc_id):
    return f"Estado del documento {doc_id}: Pendiente"

# Página de inicio de sesión y consulta de documentos
if not st.session_state.authenticated:
    st.subheader("Consultar Estado del Caso")
    
    with st.form("check_status_form"):
        doc_id = st.text_input("ID del Caso")
        check_button = st.form_submit_button("Consultar Estado")
        
        if check_button:
            if doc_id:
                status = check_document_status(doc_id)
                st.info(status)
            else:
                st.warning("Por favor, ingrese un ID del Caso")

    user_interface()
else:
    if st.session_state.role == 'administrador':
        admin_interface()
    else:
        user_interface()
