import streamlit as st
from playwright.sync_api import sync_playwright

# Simulación de credenciales para el ejemplo
credentials = st.secrets["auth"]

# Gestión de estado de la aplicación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Función para obtener el estado de cuenta utilizando Playwright
def obtener_estado_cuenta(username, password):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://acceso.web.aysa.com.ar/saml2/idp/sso/acceso.web.aysa.com.ar")
            page.fill('#username_field_id', username)  # Ajustar ID según el campo real
            page.fill('#password_field_id', password)  # Ajustar ID según el campo real
            page.click('button[type="submit"]')
            page.wait_for_load_state('networkidle')  # Esperar a que la página se cargue completamente
            estado_cuenta = page.inner_text('#elemento_estado_cuenta')  # Ajustar selector según sea necesario
            browser.close()
            return estado_cuenta
    except Exception as e:
        return f"Error al obtener el estado de la cuenta: {e}"

# Página de Inicio de Sesión
def login_page():
    st.title("Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    login_button = st.button("Iniciar sesión")
    
    if login_button:
        if username in credentials and credentials[username] == password:
            st.session_state.authenticated = True
        else:
            st.error("Usuario o contraseña incorrectos")

# Pantalla de Administración
def admin_page():
    st.title("Panel de Administración")
    st.write("¡Bienvenido, administrador!")
    
    # Ejemplo de opciones en el panel de administración
    tab1, tab2, tab3 = st.tabs(["Aysa", "Metrogas", "Edenor"])

    with tab1:
        st.write("Aysa")
        if st.button("Consultar Estado de Cuenta Aysa"):
            username = st.secrets["account"]["useraysa"]
            password = st.secrets["account"]["passaysa"]
            estado_cuenta = obtener_estado_cuenta(username, password)
            st.write(estado_cuenta)
    
    with tab2:
        st.write("Metrogas")

    with tab3:
        st.write("Edenor")
    
    if st.button("Cerrar Sesión"):
        st.session_state.authenticated = False

# Mostrar la página de inicio de sesión o el panel de administración según el estado de autenticación
if st.session_state.authenticated:
    admin_page()
else:
    login_page()