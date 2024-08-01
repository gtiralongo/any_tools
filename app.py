import streamlit as st

# Simular credenciales para el ejemplo
credentials = st.secrets["auth"]

# Gestión de estado de la aplicación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Página de Inicio de Sesión
def login_page():
    st.title("Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    login_button = st.button("Iniciar sesión")
    
    if login_button:
        if username in credentials and credentials[username] == password:
            st.session_state.authenticated = True
            st.experimental_set_query_params(authenticated=True)
        else:
            st.error("Usuario o contraseña incorrectos")

# Pantalla de Administración
def admin_page():
    st.title("Panel de Administración")
    st.write("¡Bienvenido, administrador!")
    
    # Ejemplo de opciones en el panel de administración
    if st.button("Opción 1"):
        st.write("Funcionalidad de la opción 1")
    
    if st.button("Opción 2"):
        st.write("Funcionalidad de la opción 2")
    
    if st.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.experimental_set_query_params(authenticated=False)

# Mostrar la página de inicio de sesión o el panel de administración
if st.session_state.authenticated:
    admin_page()
else:
    login_page()