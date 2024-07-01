import mysql.connector
import streamlit as st
import pandas as pd
from user_management import UserManagement

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()

def admin_interface():
    st.sidebar.subheader("Menú de Administración")
    choice = st.sidebar.radio("Seleccione una opción:", ["Ver Documentos", "Administrar Documentos", "Administrar Usuarios", "Cerrar Sesión"])
    
    if choice == "Cerrar Sesión":
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None
        st.experimental_rerun()

    elif choice == "Ver Documentos":
        st.subheader("Ver Documentos")
        casos = user_management.get_all_cases()
    
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

    elif choice == "Administrar Documentos":
        st.subheader("Administrar Documentos")
    
        case_actions_options = ["Agregar Documento", "Editar Documento", "Eliminar Documento"]
        case_action = st.sidebar.radio("Seleccione una acción:", case_actions_options)

        if case_action == "Agregar Documento":
            st.subheader("Agregar Nuevo Documento")
    
            with st.form("add_document_form"):
                code = st.text_input("Código del Documento")
                investigated_last_name = st.text_input("Apellidos del Investigado")
                investigated_first_name = st.text_input("Nombre del Investigado")
                dni = st.text_input("DNI del Investigado", max_chars=8)
        
                if len(dni) != 8 or not dni.isdigit():
                    dni = ""
        
                users = user_management.get_users()
                normal_users = [user['username'] for user in users if user['role'] == 'usuario']
                reviewer = st.selectbox("Encargado de Revisar el Documento", normal_users)

                stage = st.selectbox("Etapa del caso", ['preparatoria', 'intermedia', 'juzgamiento'])

                add_case_button = st.form_submit_button("Agregar Documento")
        
                if add_case_button:
                    st.session_state.confirmation_action = {
                        "type": "add",
                        "code": code,
                        "investigated_last_name": investigated_last_name,
                        "investigated_first_name": investigated_first_name,
                        "dni": dni,
                        "reviewer": reviewer,
                        "stage": stage
                    }
                    st.session_state.confirmation_message = f"¿Estás seguro de agregar el documento {code}?"
                    st.experimental_rerun()

        elif case_action == "Editar Documento":
            st.subheader("Editar Documento")
        
            search_criterion = st.selectbox("Buscar por", ["Encargado", "DNI"])
            if search_criterion == "Encargado":
                users = user_management.get_users()
                reviewers = [user['username'] for user in users if user['role'] == 'usuario']
                selected_reviewer = st.selectbox("Seleccione el Encargado", reviewers)
                find_case_button = st.button("Buscar casos por Encargado")

                if find_case_button:
                    st.session_state.search_criterion = "reviewer"
                    st.session_state.search_value = selected_reviewer
                    st.experimental_rerun()

            elif search_criterion == "DNI":
                search_value = st.text_input("Ingrese DNI")
                find_case_button = st.button("Buscar casos por DNI")

                if find_case_button:
                    st.session_state.search_criterion = "dni"
                    st.session_state.search_value = search_value
                    st.experimental_rerun()

            if 'search_criterion' in st.session_state:
                criterion = st.session_state.search_criterion
                value = st.session_state.search_value

                if criterion and value:
                    if criterion == "reviewer":
                        cases = user_management.get_cases_by_reviewer(value)
                    else:
                        cases = user_management.get_cases_by_dni(value)

                    if cases:
                        df = pd.DataFrame(cases)
                        df.columns = ['id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'stage']
                        st.dataframe(df)
                        selected_case_id = st.selectbox("Seleccione el Id del caso a editar", df['id'])
                        
                        if st.button("Cargar Caso"):
                            case = user_management.get_case(selected_case_id)
                            st.session_state.edit_case = case
                            st.experimental_rerun()

            if 'edit_case' in st.session_state:
                case = st.session_state.edit_case
                with st.form("edit_document_form"):
                    code = st.text_input("Código del Documento", value=case.get('code', ''))
                    investigated_last_name = st.text_input("Apellidos del Investigado", value=case.get('investigated_last_name', ''))
                    investigated_first_name = st.text_input("Nombre del Investigado", value=case.get('investigated_first_name', ''))
                    dni = st.text_input("DNI del Investigado", value=case.get('dni', ''), max_chars=8)
            
                    if len(dni) != 8 or not dni.isdigit():
                        st.warning("DNI inválido")
                        dni = ""
            
                    users = user_management.get_users()
                    normal_users = [user['username'] for user in users if user['role'] == 'usuario']
                    reviewer = st.selectbox("Encargado de Revisar el Documento", normal_users, index=normal_users.index(case.get('reviewer', '')))

                    stage = st.selectbox("Etapa del Caso", ['preparatoria', 'intermedia', 'juzgamiento'], index=['preparatoria', 'intermedia', 'juzgamiento'].index(case.get('stage', 'preparatoria')))
                    edit_case_button = st.form_submit_button("Actualizar Caso")
            
                    if edit_case_button and dni:
                        st.session_state.confirmation_action = {
                            "type": "edit",
                            "id": case['id'],
                            "code": code,
                            "investigated_last_name": investigated_last_name,
                            "investigated_first_name": investigated_first_name,
                            "dni": dni,
                            "reviewer": reviewer,
                            "stage": stage
                        }
                        st.session_state.confirmation_message = f"¿Estás seguro de actualizar el documento {code}?"
                        st.experimental_rerun()

        elif case_action == "Eliminar Documento":
            st.subheader("Eliminar Documento")

            search_criterion = st.selectbox("Buscar por", ["Encargado", "DNI"])
            if search_criterion == "Encargado":
                users = user_management.get_users()
                reviewers = [user['username'] for user in users if user['role'] == 'usuario']
                selected_reviewer = st.selectbox("Seleccione el Encargado", reviewers)
                find_case_button = st.button("Buscar casos por Encargado")

                if find_case_button:
                    st.session_state.search_criterion = "reviewer"
                    st.session_state.search_value = selected_reviewer
                    st.experimental_rerun()

            elif search_criterion == "DNI":
                search_value = st.text_input("Ingrese DNI")
                find_case_button = st.button("Buscar casos por DNI")

                if find_case_button:
                    st.session_state.search_criterion = "dni"
                    st.session_state.search_value = search_value
                    st.experimental_rerun()

            if 'search_criterion' in st.session_state:
                criterion = st.session_state.search_criterion
                value = st.session_state.search_value

                if criterion and value:
                    if criterion == "reviewer":
                        cases = user_management.get_cases_by_reviewer(value)
                    else:
                        cases = user_management.get_cases_by_dni(value)

                    if cases:
                        df = pd.DataFrame(cases)
                        df.columns = ['id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'stage']
                        st.dataframe(df)
                        selected_case_id = st.selectbox("Seleccione el Id del caso a eliminar", df['id'])
                        
                        if st.button("Eliminar Caso"):
                            st.session_state.confirmation_action = {
                                "type": "delete",
                                "id": selected_case_id
                            }
                            st.session_state.confirmation_message = f"¿Estás seguro de eliminar el caso con ID {selected_case_id}?"
                            st.experimental_rerun()

    elif choice == "Administrar Usuarios":
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
                        st.session_state.confirmation_action = {
                            "type": "add_user",
                            "username": username,
                            "password": password,
                            "role": role,
                            "first_name": first_name,
                            "last_name": last_name,
                            "dni": dni
                        }
                        st.session_state.confirmation_message = f"¿Estás seguro de agregar al usuario {username}?"
                        st.experimental_rerun()
                    else:
                        st.warning("Por favor, ingrese un DNI válido de 8 dígitos.")

        elif user_action == "Editar Usuario":
            st.subheader("Editar Usuario")

            with st.form("find_user_form"):
                search_type = st.radio(
                    "Buscar usuario por:",
                    ('Apellido', 'Nombre')
                )
        
                if search_type == 'Apellido':
                    last_name = st.text_input("Apellido de Usuario a Editar")
                    find_user_button = st.form_submit_button("Buscar Usuario")
                    if find_user_button:
                        user = user_management.get_user_by_last_name(last_name)
                        if user:
                            st.session_state.edit_user = user
                            st.experimental_rerun()
                        else:
                            st.warning(f"No se encontró un usuario con apellido {last_name}")
                elif search_type == 'Nombre':
                    first_name = st.text_input("Nombre del Usuario a Editar")
                    find_user_button = st.form_submit_button("Buscar Usuario")
                    if find_user_button:
                        user = user_management.get_user_by_first_name(first_name)
                        if user:
                            st.session_state.edit_user = user
                            st.experimental_rerun()
                        else:
                            st.warning(f"No se encontró un usuario con nombre {first_name}")

            if 'edit_user' in st.session_state:
                user = st.session_state.edit_user
                with st.form("edit_user_form"):
                    new_first_name = st.text_input("Nuevo Nombre", value=user['first_name'])
                    new_last_name = st.text_input("Nuevo Apellido", value=user['last_name'])
                    new_dni = st.text_input("Nuevo DNI", value=user['dni'])
                    new_role = st.text_input("Nuevo Rol", value=user['role'])
                    new_password = st.text_input("Nueva Contraseña", type='password')
                    submit_button = st.form_submit_button("Actualizar Usuario")
            
                    if submit_button:
                        st.session_state.confirmation_action = {
                            "type": "edit_user",
                            "username": user['username'],
                            "password": new_password,
                            "role": new_role,
                            "first_name": new_first_name,
                            "last_name": new_last_name,
                            "dni": new_dni
                        }
                        st.session_state.confirmation_message = f"¿Estás seguro de actualizar al usuario {user['username']}?"
                        st.experimental_rerun()

        elif user_action == "Eliminar Usuario":
            st.subheader("Eliminar Usuario")
            with st.form("delete_user_form"):
                username = st.text_input("Nombre de Usuario a Eliminar")
                delete_user_button = st.form_submit_button("Eliminar Usuario")

                if delete_user_button:
                    user = user_management.get_user_by_username(username)
                    if user:
                        st.session_state.confirmation_action = {
                            "type": "delete_user",
                            "username": username
                        }
                        st.session_state.confirmation_message = f"¿Estás seguro de eliminar al usuario {username}?"
                        st.experimental_rerun()
                    else:
                        st.warning(f"No se encontró un usuario con nombre {username}")

    if 'confirmation_message' in st.session_state:
        st.warning(st.session_state.confirmation_message)
        accept_button = st.button("Aceptar")
        cancel_button = st.button("Cancelar")

        if accept_button:
            action = st.session_state.confirmation_action
            if action['type'] == "add":
                user_management.create_case(action['code'], action['investigated_last_name'], action['investigated_first_name'], action['dni'], action['reviewer'], action['stage'])
                st.success(f"Documento {action['code']} agregado exitosamente")
            elif action['type'] == "edit":
                user_management.update_case(action['code'], action['code'], action['investigated_last_name'], action['investigated_first_name'], action['dni'], action['reviewer'], action['stage'])
                st.success(f"Caso {action['code']} actualizado exitosamente")
            elif action['type'] == "delete":
                user_management.delete_case(action['code'])
                st.success(f"Caso {action['code']} eliminado exitosamente")
            elif action['type'] == "add_user":
                user_management.create_user(action['username'], action['password'], action['role'], action['first_name'], action['last_name'], action['dni'])
                st.success(f"Usuario {action['username']} agregado exitosamente")
            elif action['type'] == "edit_user":
                user_management.update_user(action['username'], action['password'], action['role'], action['first_name'], action['last_name'], action['dni'])
                st.success(f"Usuario {action['username']} actualizado correctamente")
            elif action['type'] == "delete_user":
                user_management.delete_user(action['username'])
                st.success(f"Usuario {action['username']} eliminado exitosamente")
            st.session_state.pop('confirmation_message')
            st.session_state.pop('confirmation_action')
            st.experimental_rerun()

        if cancel_button:
            st.session_state.pop('confirmation_message')
            st.session_state.pop('confirmation_action')
            st.experimental_rerun()
