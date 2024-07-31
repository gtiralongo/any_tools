import streamlit as st

# Leer las credenciales desde el archivo secrets
credentials = st.secrets["auth"]

# Título de la aplicación
st.title("Iniciar Sesión")

# Formulario de inicio de sesión
username = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")
login_button = st.button("Iniciar sesión")

# Verificar credenciales
if login_button:
    if username in credentials and credentials[username] == password:
        st.success("Inicio de sesión exitoso")
        # Aquí puedes continuar con la lógica de tu aplicación
    else:
        st.error("Usuario o contraseña incorrectos")
