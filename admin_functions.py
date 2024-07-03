import streamlit as st
import pandas as pd
from user_management import UserManagement

# Inicializar la gestión de usuarios y casos
user_management = UserManagement()

# CSS para expandir el ancho de los elementos
st.markdown("""
    <style>
    .main .block-container {
        padding: 1rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def admin_interface():
    st.sidebar.subheader("Menú de Administración")
    choice = st.sidebar.radio("Seleccione una opción:", ["Ver Casos", "Administrar Casos", "Administrar Usuarios", "Cerrar Sesión"])
    
    if choice == "Cerrar Sesión":
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None
        st.experimental_rerun()

    elif choice == "Ver Casos":
        st.subheader("Ver Casos")
        casos = user_management.get_all_cases()
    
        if casos:
            df = pd.DataFrame(casos)
            df.columns = ['case_id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'stage']
            df = df.rename(columns={
                'case_id': 'ID',
                'code': 'Código del Caso',
                'investigated_last_name': 'Apellidos del Investigado',
                'investigated_first_name': 'Nombre del Investigado',
                'dni': 'DNI del Investigado',
                'reviewer': 'Encargado de Revisar el Caso',
                'stage': 'Etapa',
            })

            for i, row in df.iterrows():
                cols = st.columns((3, 10, 15, 15, 8, 10, 11))
                cols[0].write(row['ID'])
                cols[1].write(row['Código del Caso'])
                cols[2].write(row['Apellidos del Investigado'])
                cols[3].write(row['Nombre del Investigado'])
                cols[4].write(row['DNI del Investigado'])
                cols[5].write(row['Encargado de Revisar el Caso'])
                cols[6].write(row['Etapa'])
        else:
            st.warning("No hay casos disponibles para mostrar.")

    elif choice == "Administrar Casos":
        st.subheader("Administrar Casos")

        case_actions_options = ["Agregar Caso", "Modificar Caso"]
        case_action = st.sidebar.radio("Seleccione una acción:", case_actions_options)

        if case_action == "Agregar Caso":
            st.subheader("Agregar Nuevo Caso")
    
            with st.form("add_case_form"):
                code = st.text_input("Código del Caso")
                investigated_last_name = st.text_input("Apellidos del Investigado")
                investigated_first_name = st.text_input("Nombre del Investigado")
                dni = st.text_input("DNI del Investigado", max_chars=8)
        
                if len(dni) != 8 or not dni.isdigit():
                    dni = ""
        
                users = user_management.get_users()
                normal_users = [user['username'] for user in users if user['role'] == 'usuario']
                reviewer = st.selectbox("Encargado de Revisar el Caso", normal_users)

                stage = st.selectbox("Etapa del caso", ['preparatoria', 'intermedia', 'juzgamiento'])

                add_case_button = st.form_submit_button("Agregar Caso")
        
                if add_case_button:
                    if dni:
                        user_management.create_case(code, investigated_last_name, investigated_first_name, dni, reviewer, stage)
                        st.success(f"Caso {code} agregado exitosamente")
                        st.experimental_rerun()

        elif case_action == "Modificar Caso":
            st.subheader("Editar o Eliminar Caso")

            casos = user_management.get_all_cases()
            if casos:
                df = pd.DataFrame(casos)
                df.columns = ['case_id', 'code', 'investigated_last_name', 'investigated_first_name', 'dni', 'reviewer', 'stage']
                df = df.rename(columns={
                    'case_id': 'ID',
                    'code': 'Código',
                    'investigated_last_name': 'Apellidos',
                    'investigated_first_name': 'Nombres',
                    'dni': 'DNI',
                    'reviewer': 'Encargado',
                    'stage': 'Etapa',
                })

                for i, row in df.iterrows():
                    cols = st.columns((3, 10, 15, 15, 8, 10, 11, 5, 5))
                    cols[0].write(row['ID'])
                    cols[1].write(row['Código'])
                    cols[2].write(row['Apellidos'])
                    cols[3].write(row['Nombres'])
                    cols[4].write(row['DNI'])
                    cols[5].write(row['Encargado'])
                    cols[6].write(row['Etapa'])
                    edit_button = cols[7].button("✏️", key=f"edit_{row['ID']}")
                    delete_button = cols[8].button("🗑️", key=f"delete_{row['ID']}")
                    
                    if edit_button:
                        st.session_state.edit_case = user_management.get_case(row['ID'])
                        st.experimental_rerun()
                    
                    if delete_button:
                        user_management.delete_case(row['ID'])
                        st.success(f"Caso con ID {row['ID']} eliminado exitosamente")
                        st.experimental_rerun()

            else:
                st.warning("No hay casos disponibles para mostrar.")

            if 'edit_case' in st.session_state:
                case = st.session_state.edit_case
                with st.form("edit_case_form"):
                    code = st.text_input("Código del Caso", value=case.get('code', ''))
                    investigated_last_name = st.text_input("Apellidos del Investigado", value=case.get('investigated_last_name', ''))
                    investigated_first_name = st.text_input("Nombre del Investigado", value=case.get('investigated_first_name', ''))
                    dni = st.text_input("DNI del Investigado", value=case.get('dni', ''), max_chars=8)
            
                    if len(dni) != 8 or not dni.isdigit():
                        st.warning("DNI inválido")
                        dni = ""
            
                    users = user_management.get_users()
                    normal_users = [user['username'] for user in users if user['role'] == 'usuario']
                    reviewer = st.selectbox("Encargado de Revisar el Caso", normal_users, index=normal_users.index(case.get('reviewer', '')))

                    stage = st.selectbox("Etapa del Caso", ['preparatoria', 'intermedia', 'juzgamiento'], index=['preparatoria', 'intermedia', 'juzgamiento'].index(case.get('stage', 'preparatoria')))
                    edit_case_button = st.form_submit_button("Actualizar Caso")

                    if edit_case_button and dni:
                        user_management.update_case(case['case_id'], code, investigated_last_name, investigated_first_name, dni, reviewer, stage)
                        st.success(f"Caso {code} actualizado exitosamente")
                        st.session_state.pop('edit_case')
                        st.experimental_rerun()

    elif choice == "Administrar Usuarios":
        st.subheader("Administrar Usuarios")

        user_actions_options = ["Agregar Usuario", "Modificar Usuario"]
        user_action = st.sidebar.radio("Seleccione una acción:", user_actions_options)

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
                        st.experimental_rerun()
                    else:
                        st.warning("Por favor, ingrese un DNI válido de 8 dígitos.")

        elif user_action == "Modificar Usuario":
            st.subheader("Editar o Eliminar Usuario")

            usuarios = user_management.get_users()
            if usuarios:
                df = pd.DataFrame(usuarios)
                df.columns = ['user_id', 'username', 'password', 'role', 'first_name', 'last_name', 'dni']
                df = df.rename(columns={
                    'user_id': 'ID',
                    'username': 'Nombre de Usuario',
                    'password': 'Contraseña',
                    'role': 'Rol',
                    'first_name': 'Nombres',
                    'last_name': 'Apellidos',
                    'dni': 'DNI',
                })

                for i, row in df.iterrows():
                    cols = st.columns((3, 10, 10, 13, 20, 20, 8, 6, 7))
                    cols[0].write(row['ID'])
                    cols[1].write(row['Nombre de Usuario'])
                    cols[2].write(row['Contraseña'])
                    cols[3].write(row['Rol'])
                    cols[4].write(row['Nombres'])
                    cols[5].write(row['Apellidos'])
                    cols[6].write(row['DNI'])
                    edit_button = cols[7].button("✏️", key=f"edit_{row['Nombre de Usuario']}")
                    delete_button = cols[8].button("🗑️", key=f"delete_{row['Nombre de Usuario']}")
                    
                    if edit_button:
                        st.session_state.edit_user = user_management.get_user_by_username(row['Nombre de Usuario'])
                        st.experimental_rerun()
                    
                    if delete_button:
                        user_management.delete_user(row['Nombre de Usuario'])
                        st.success(f"Usuario {row['Nombre de Usuario']} eliminado exitosamente")
                        st.experimental_rerun()

            else:
                st.warning("No hay usuarios disponibles para mostrar.")

            if 'edit_user' in st.session_state:
                user = st.session_state.edit_user
                with st.form("edit_user_form"):
                    new_first_name = st.text_input("Nuevo Nombre", value=user['first_name'])
                    new_last_name = st.text_input("Nuevo Apellido", value=user['last_name'])
                    new_dni = st.text_input("Nuevo DNI", value=user['dni'])
                    new_role = st.selectbox("Nuevo Rol", ["administrador", "usuario"], index=["administrador", "usuario"].index(user['role']))
                    new_password = st.text_input("Nueva Contraseña", type='password')
                    submit_button = st.form_submit_button("Actualizar Usuario")
            
                    if submit_button:
                        user_management.update_user(
                            user_id=user['user_id'],
                            username=user['username'],
                            password=new_password,
                            role=new_role,
                            first_name=new_first_name,
                            last_name=new_last_name,
                            dni=new_dni
                        )
                        st.success("Usuario actualizado correctamente")
                        del st.session_state.edit_user
                        st.experimental_rerun()

# Llama a la función de interfaz de administrador
admin_interface()
