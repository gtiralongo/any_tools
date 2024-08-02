import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Simulación de credenciales para el ejemplo
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
        # Configuración de opciones del navegador
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--start-maximized")

        # Iniciar el navegador
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        def iniciar_sesion(driver, usuario, contrasena):
            # Navegar a la página de inicio de sesión
            driver.get("https://oficinavirtual.web.aysa.com.ar/auth/index.html?#Accesos/")
            time.sleep(2)

            # Ingresar el usuario
            driver.find_element(By.ID, "j_username").send_keys(usuario)
            # Ingresar la contraseña
            driver.find_element(By.ID, "j_password").send_keys(contrasena)
            # Presionar Enter para iniciar sesión
            driver.find_element(By.ID, "j_password").send_keys(Keys.ENTER)
            time.sleep(1)

        def navegar_estado_cuenta(driver):
            # Navegar a la página de estado de cuenta
            driver.get("https://portal.web.aysa.com.ar/index.html#/estadocuenta")
            time.sleep(20)

        def obtener_datos_cuenta(driver):
            try:
                id_vencimiento_agua = driver.find_element(By.ID, "__text50-__clone0")
                vencimiento_text = id_vencimiento_agua.text
                id_monto_agua = driver.find_element(By.ID, "__text52-__clone0")
                monto_text = id_monto_agua.text
            except:
                print(driver.find_element(By.TAG_NAME,"body"))

            # return vencimiento_text, monto_text
            return print(driver.find_element(By.TAG_NAME,"body")) 
                

        
        usuario = st.secrets["account"]["useraysa"]  # Reemplaza con tu usuario
        contrasena = st.secrets["account"]["passaysa"]  # Reemplaza con tu contraseña
        try:
            iniciar_sesion(driver, usuario, contrasena)
            navegar_estado_cuenta(driver)
            obtener_datos_cuenta(driver)
            # vencimiento_text, monto_text = obtener_datos_cuenta(driver)
            
            # # Formatear y mostrar el mensaje
            # mensaje = f"💧*Agus:* 📅: _{vencimiento_text}_ 💸: _{monto_text}_ [🧾](https://portal.web.aysa.com.ar/index.html#/facturas)"
            # print(mensaje)
            driver.quit()
        except:
            driver.quit()

                        
    
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



# if __name__ == "__main__":
#     main()




