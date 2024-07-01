# admin_functions.py
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

                add_case_botton = st.form_submit_button("Agregar Documento")
        
                if add_case_botton:
                    if dni:
                        user_management.create_case(code, investigated_last_name, investigated_first_name, dni, reviewer, stage)
                        st.success(f"Documento {code} agregado exitosamente")

        elif case_action == "Editar Documento":
            st.subheader("Editar Documento")
        
            with st.form("find_document_form"):
                search_criterion = st.selectbox("Buscar por", ["Encargado", "DNI"])
                if search_criterion == "Encargado":
                    users = user_management.get_users()
                    reviewers = [user['username'] for user in users if user['role'] == 'usuario']
                    selected_reviewer = st.selectbox("Seleccione el Encargado", reviewers)
                else:
                    search_value = st.text_input(f"Ingrese {search_criterion}")

                find_case_botton = st.form_submit_button("Buscar caso")

        
            if find_case_botton:
                criterio_map = {
                    "Encargado" : "reviewer",
                    "DNI" : "dni"
                }
                criterion = criterio_map.get(search_criterion)

                if criterion == "reviewer":
                    cases = user_management.get_cases_by_reviewer(selected_reviewer)

                    if cases:
                        df = pd.DataFrame(cases)
                        st.dataframe(df)
                        selected_case_id = st.selectbox("Seleccione el Id del caso a editar", df['id'])
                        if st.button("Cargar Caso"):
                            case = user_management.get_case(selected_case_id)
                            st.session_state.edit_case = case
                    else:
                        st.warning(f"No se encontraron casos para el encargado {selected_reviewer}")
            
                else: 
                    cases = user_management.get_cases_by_dni(search_value)
                    if cases:
                        if len(cases) > 1:
                            df = pd.DataFrame(cases)
                            st.dataframe(df)
                            selected_case_id = st.selectbox("Seleccione el Id del caso a editar", df['id'])
                            if st.button("Cargar Caso"):
                                case = user_management.get_case(selected_case_id)
                                st.session_state.edit_case = case
                        else:
                            case = cases[0]
                            st.session_state.edit_case = case
                    else:
                        st.warning(f"No se encontró un caso con el DNI {search_value}")

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

                    stage = st.selectbox("Etapa del Caso", ['Preparatoria', 'Intermedia', 'Juzgamiento'], index=['preparatoria', 'intermedia', 'juzgamiento'].index(case.get('stage', 'preparatoria')))
                    edit_cas_button = st.form_submit_button("Actualizar Caso")
            
                    if edit_cas_button and dni:
                        user_management.update_case(case['id'], code, investigated_last_name, investigated_first_name, dni, reviewer, stage)
                        st.success(f"Caso {code} actualizado exitosamente")
                        st.session_state.pop('edit_case')

        elif case_action == "Eliminar Documento":
            st.subheader("Eliminar Documento")

            with st.form("find_document_form"):
                search_criterion = st.selectbox("Buscar por", ["Encargado", "DNI"])
                if search_criterion == "Encargado":
                    users = user_management.get_users()
                    reviewers = [user['username'] for user in users if user['role'] == 'usuario']
                    selected_reviewer = st.selectbox("Seleccione el Encargado", reviewers)
                else:
                    search_value = st.text_input(f"Ingrese {search_criterion}")

                find_case_botton = st.form_submit_button("Buscar caso")

        
            if find_case_botton:
                criterio_map = {
                    "Encargado" : "reviewer",
                    "DNI" : "dni"
                }
                criterion = criterio_map.get(search_criterion)

                if criterion == "reviewer":
                    cases = user_management.get_cases_by_reviewer(selected_reviewer)

                    if cases:
                        df = pd.DataFrame(cases)
                        selected_case_id = st.selectbox("Seleccione el Id del caso a eliminar", df['id'])
                        if st.button("Eliminar Caso"):
                            confirmation = st.checkbox(f"Confirmar eliminación del caso con ID {selected_case_id}")
                            if confirmation:
                                user_management.delete_case(selected_case_id)
                                st.success(f"Caso con ID {selected_case_id} eliminado exitosamente")
                            else:
                                st.warning("Eliminación cancelada")
                    else:
                        st.warning(f"No se encontraron casos para el encargado {selected_reviewer}")
                elif criterion == "dni":
                    cases = user_management.get_cases_by_dni(search_value)
                    if cases:
                        if len(cases) > 1:
                            df = pd.DataFrame(cases)
                            st.dataframe(df)
                            selected_case_id = st.selectbox("Seleccione el Id del caso a eliminar", df['id'])
                            if st.button("Eliminar Caso"):
                                confirmation = st.checkbox(f"Confirmar eliminación del caso con ID {selected_case_id}")
                                if confirmation:
                                    user_management.delete_case(selected_case_id)
                                    st.success(f"Caso con ID {selected_case_id} eliminado exitosamente")
                                else:
                                    st.warning("Eliminación cancelada")
                        
                        else:
                            case = cases[0]
                            st.session_state.edit_case = case  # Actualizar el estado edit_case
                            confirmation = st.checkbox(f"Confirmar eliminación del caso con ID {case['id']}")
                            if confirmation:
                                user_management.delete_case(case['id'])
                                st.success(f"Caso con ID {case['id']} eliminado exitosamente")
                            else:
                                st.warning("Eliminación cancelada")
                    else:
                        st.warning(f"No se encontró un caso con el DNI {search_value}")

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
                        user_management.create_user(username, password, role, first_name, last_name, dni)
                        st.success(f"Usuario {username} agregado exitosamente")
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
                        else:
                            st.warning(f"No se encontró un usuario con apellido {last_name}")
                elif search_type == 'Nombre':
                    first_name = st.text_input("Nombre del Usuario a Editar")
                    find_user_button = st.form_submit_button("Buscar Usuario")
                    if find_user_button:
                        user = user_management.get_user_by_first_name(first_name)
                        if user:
                            st.session_state.edit_user = user
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
                        user_management.update_user(
                            username=user['username'],
                            password=new_password,
                            role=new_role,
                            first_name=new_first_name,
                            last_name=new_last_name,
                            dni=new_dni
                        )
                        st.success("Usuario actualizado correctamente")
                        del st.session_state.edit_user


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
