import streamlit as st
import pandas as pd
from user_management import UserManagement

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
st.title("Sistema de Gestión de Documentos")

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

# Página de inicio de sesión y consulta de documentos
if not st.session_state.authenticated:
    st.subheader("Consultar Estado del Documento")
    
    with st.form("check_status_form"):
        doc_id = st.text_input("ID del Documento")
        check_button = st.form_submit_button("Consultar Estado")
        
        if check_button:
            if doc_id:
                status = check_document_status(doc_id)
                st.info(status)
            else:
                st.warning("Por favor, ingrese un ID de documento")
    
    st.sidebar.subheader("Iniciar Sesión")
    
    with st.sidebar.form("login_form"):
        username = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type='password')
        login_button = st.form_submit_button("Iniciar Sesión")
        
        if login_button:
            login(username, password)
else:
    # Página de administración de documentos y usuarios
    st.sidebar.subheader("Menú de Administración")
    
    if st.session_state.role == 'administrador':
        choice = st.sidebar.radio("Seleccione una opción:", ["Ver Documentos", "Administrar Documentos", "Administrar Usuarios", "Cerrar Sesión"])
    else:
        choice = st.sidebar.radio("Seleccione una opción:", ["Ver Documentos", "Administrar Documentos", "Administrar Mi Usuario", "Cerrar Sesión"])

    if choice == "Cerrar Sesión":
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None
        st.experimental_rerun()

    elif choice == "Ver Documentos":
        st.subheader("Ver Documentos")
    
        if st.session_state.role == 'administrador':
            documents = user_management.get_all_cases()
        else:
            documents = user_management.get_cases_by_reviewer(st.session_state.username)
    
        if documents:
            df = pd.DataFrame(documents)
            df.columns = ['id', 'code', 'investigator_last_name', 'investigator_first_name', 'dni', 'reviewer', 'description', 'created_at', 'stage', 'deadline', 'status', 'urgency_level', 'review_file']
            df = df.rename(columns={
                'id': 'ID',
                'code': 'Código del Documento',
                'investigator_last_name': 'Apellidos del Investigado',
                'investigator_first_name': 'Nombre del Investigado',
                'dni': 'DNI del Investigado',
                'reviewer': 'Encargado de Revisar el Documento',
                'stage': 'Etapa',
            })
            st.dataframe(df)
        else:
            st.warning("No hay documentos disponibles para mostrar.")

    elif choice == "Administrar Documentos":
        st.subheader("Administrar Documentos")
    
        if st.session_state.role == 'administrador':
            doc_action_options = ["Agregar Documento", "Editar Documento", "Eliminar Documento"]
        else:
            doc_action_options = ["Agregar Documento", "Editar Documento"]
    
        doc_action = st.sidebar.radio("Seleccione una acción:", doc_action_options)

        if doc_action == "Agregar Documento":
            st.subheader("Agregar Nuevo Documento")
    
            with st.form("add_document_form"):
                doc_code = st.text_input("Código del Documento")
                last_name = st.text_input("Apellidos del Investigado")
                first_name = st.text_input("Nombre del Investigado")
                dni = st.text_input("DNI del Investigado", max_chars=8)
        
                if len(dni) != 8 or not dni.isdigit():
                    dni = ""
        
                users = user_management.get_users()
                normal_users = [user['username'] for user in users if user['role'] == 'usuario']
                reviewer = st.selectbox("Encargado de Revisar el Documento", normal_users)

                stage = st.selectbox("Etapa del caso", ['preparatoria', 'intermedia', 'juzgamiento'])

                add_doc_button = st.form_submit_button("Agregar Documento")
        
                if add_doc_button:
                    if dni:
                        user_management.create_case(doc_code, last_name, first_name, dni, reviewer, stage)
                        st.success(f"Documento {doc_code} agregado exitosamente")

        elif doc_action == "Editar Documento":
            st.subheader("Editar Documento")
        
            with st.form("find_document_form"):
                doc_id = st.text_input("ID del Documento a Editar")
                find_doc_button = st.form_submit_button("Buscar Documento")
        
            if find_doc_button:
                document = user_management.get_document_by_id(doc_id)
                if document:
                    st.session_state.edit_document = document
                else:
                    st.warning(f"No se encontró un documento con ID {doc_id}")

            if 'edit_document' in st.session_state:
                document = st.session_state.edit_document
                with st.form("edit_document_form"):
                    doc_code = st.text_input("Código del Documento", value=document.get('doc_code', ''))
                    last_name = st.text_input("Apellidos del Investigado", value=document.get('last_name', ''))
                    first_name = st.text_input("Nombre del Investigado", value=document.get('first_name', ''))
                    dni = st.text_input("DNI del Investigado", value=document.get('dni', ''), max_chars=8)
            
                    if len(dni) != 8 or not dni.isdigit():
                        st.warning("DNI inválido")
                        dni = ""
            
                    users = user_management.get_users()
                    normal_users = [user['username'] for user in users if user['role'] == 'usuario']
                    reviewer = st.selectbox("Encargado de Revisar el Documento", normal_users, index=normal_users.index(document.get('reviewer', '')))

                    doc_content = st.text_area("Contenido del Documento", value=document.get('content', ''))
                    edit_doc_button = st.form_submit_button("Actualizar Documento")
            
                    if edit_doc_button and dni:
                        user_management.update_document(document['id'], doc_code, last_name, first_name, dni, reviewer, doc_content)
                        st.success(f"Documento {doc_code} actualizado exitosamente")
                        st.session_state.pop('edit_document')

        elif doc_action == "Eliminar Documento":
            st.subheader("Eliminar Documento")

            with st.form("delete_document_form"):
                doc_id = st.text_input("ID del Documento a Eliminar")
                delete_doc_button = st.form_submit_button("Eliminar Documento")

                if delete_doc_button:
                    document = user_management.get_document_by_id(doc_id)
                    if document:
                        user_management.delete_document(document['id'])
                        st.success(f"Documento con ID {doc_id} eliminado exitosamente")
                    else:
                        st.warning(f"No se encontró un documento con ID {doc_id}")

    elif choice == "Administrar Usuarios" and st.session_state.role == 'administrador':
        st.subheader("Administrar Usuarios")
        user_action = st.sidebar.radio("Seleccione una acción:", ["Agregar Usuario", "Editar Usuario", "Eliminar Usuario"])

        if user_action == "Agregar Usuario":
            st.subheader("Agregar Nuevo Usuario")
            with st.form("add_user_form"):
                first_name = st.text_input("Nombres")
                last_name = st.text_input("Apellidos")
                dni = st.text_input("DNI", max_chars=8)
                username = st.text_input("Nombre de Usuario")
                password = st.text_input("Contraseña", type='password')
                role = st.selectbox("Rol", ["administrador", "usuario"])
                add_user_button = st.form_submit_button("Agregar Usuario")

                if add_user_button:
                    if len(dni) == 8 and dni.isdigit():
                        user_management.create_user(username, password, role, first_name, last_name, dni)
                        st.success(f"Usuario {username} agregado exitosamente")
                    else:
                        st.warning("Por favor, ingrese un DNI válido de 8 dígitos.")

        elif user_action == "Editar Usuario":
            st.subheader("Editar Usuario")
            with st.form("find_user_form"):
                username = st.text_input("Nombre de Usuario a Editar")
                find_user_button = st.form_submit_button("Buscar Usuario")

                if find_user_button:
                    user = user_management.get_user_by_username(username)
                    if user:
                        st.session_state.edit_user = user
                    else:
                        st.warning(f"No se encontró un usuario con nombre {username}")

            if 'edit_user' in st.session_state:
                user = st.session_state.edit_user
                with st.form("edit_user_form"):
                    username = st.text_input("Nombre de Usuario", value=user.get('username', ''))
                    password = st.text_input("Nueva Contraseña", type='password')
                    role = st.selectbox("Rol", ["administrador", "usuario"], index=["administrador", "usuario"].index(user.get('role', 'usuario')))
                    first_name = st.text_input("Nombres", value=user.get('first_name', ''))
                    last_name = st.text_input("Apellidos", value=user.get('last_name', ''))
                    dni = st.text_input("DNI", value=user.get('dni', ''), max_chars=8)
            
                    edit_user_button = st.form_submit_button("Actualizar Usuario")
            
                    if edit_user_button:
                        if len(dni) == 8 and dni.isdigit():
                            user_management.update_user(username, password, role, first_name, last_name, dni)
                            st.success(f"Usuario {username} actualizado exitosamente")
                            st.session_state.pop('edit_user')

        elif user_action == "Eliminar Usuario":
            st.subheader("Eliminar Usuario")
            with st.form("delete_user_form"):
                username = st.text_input("Nombre de Usuario a Eliminar")
                delete_user_button = st.form_submit_button("Eliminar Usuario")

                if delete_user_button:
                    user = user_management.get_user_by_username(username)
                    if user:
                        user_management.delete_user(username)
                        st.success(f"Usuario {username} eliminado exitosamente")
                    else:
                        st.warning(f"No se encontró un usuario con nombre {username}")