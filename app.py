import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
import base64
from PIL import Image
import io

# Función para convertir imagen a base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Función para agregar el logo a un archivo PDF
def add_logo_to_pdf(pdf, logo_path):
    pdf.image(logo_path, x=10, y=8, w=30)  # Ajustar la posición (x, y) y tamaño (w) del logo

# Función para generar el PDF y guardarlo en un archivo temporal
def generar_pdf(escuela, modalidad, tabla_gramatica, tabla_vocabulario, file_path, logo_path):
    pdf = FPDF()
    pdf.add_page()

    # Añadir logo en la parte superior
    add_logo_to_pdf(pdf, logo_path)

    # Título principal
    pdf.set_font("Arial", size=12)
    pdf.ln(20)  # Espacio después del logo
    pdf.cell(200, 10, txt="Resultados de la Prueba Estatal de Inglés", ln=True, align="C")
    pdf.ln(10)
    
    # Información de la escuela
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Escuela: {escuela}", ln=True)
    pdf.cell(200, 10, txt=f"Modalidad: {modalidad}", ln=True)
    pdf.ln(10)

    # Añadir tablas de frecuencias con porcentaje
    pdf.set_font("Arial", size=10)
    
    pdf.cell(100, 10, txt="Tabla de Frecuencias: Gramática", ln=True)
    pdf.ln(5)
    pdf.cell(80, 10, txt="Nivel", border=1)
    pdf.cell(40, 10, txt="Estudiantes", border=1)
    pdf.cell(40, 10, txt="Porcentaje", border=1)
    pdf.ln()
    for i in range(len(tabla_gramatica)):
        pdf.cell(80, 10, txt=f"{tabla_gramatica.iloc[i]['Nivel']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_gramatica.iloc[i]['Estudiantes']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_gramatica.iloc[i]['Porcentaje']:.2f}%", border=1)
        pdf.ln()
    pdf.ln(10)

    pdf.cell(100, 10, txt="Tabla de Frecuencias: Vocabulario", ln=True)
    pdf.ln(5)
    pdf.cell(80, 10, txt="Nivel", border=1)
    pdf.cell(40, 10, txt="Estudiantes", border=1)
    pdf.cell(40, 10, txt="Porcentaje", border=1)
    pdf.ln()
    for i in range(len(tabla_vocabulario)):
        pdf.cell(80, 10, txt=f"{tabla_vocabulario.iloc[i]['Nivel']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_vocabulario.iloc[i]['Estudiantes']}", border=1)
        pdf.cell(40, 10, txt=f"{tabla_vocabulario.iloc[i]['Porcentaje']:.2f}%", border=1)
        pdf.ln()
    
    # Ajustar posición para pie de página
    pdf.set_y(-30)  # Ajusta esta posición para mover el pie de página

    # Añadir la leyenda al final de la página
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 10, txt="La información proporcionada en esta página es suministrada por el Centro de Evaluación Educativa del Estado de Yucatán con fines exclusivamente informativos", align='C')

    # Guardar el PDF en un archivo temporal
    pdf.output(file_path)

# Cargar datos desde la ruta especificada
df = pd.read_csv('D:\\Phyton\\Pruebas\\PEI-1\\Resultados.csv')

# Configuración de la página
st.set_page_config(page_title="Resultados de la Prueba Estatal de Inglés", layout="wide")

# Convertir la imagen del logo a base64
logo_path = "D:\\Phyton\\Pruebas\\PEI-1\\logo.png"
logo_base64 = image_to_base64(logo_path)

# Mostrar el logo en la parte superior izquierda con tamaño ajustado
st.markdown(
    f"""
    <div style='display: flex; align-items: center;'>
        <img src="data:image/png;base64,{logo_base64}" width="235" height="56" style="margin-right: 15px;">
        <h1>Resultados de la Prueba Estatal de Inglés</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Filtro por CCT
cct_input = st.text_input("Escribe el CCT:")

# Filtrar DataFrame según el valor de CCT ingresado
df_filtered = df[df['CCT'] == cct_input]

# Lista de categorías en orden deseado
categorias_ordenadas = ['Pre A1', 'A1', 'A2', 'Superior a A2']

if not df_filtered.empty:
    # Mostrar Escuela y Modalidad asociadas al CCT
    escuela = df_filtered['Escuela'].iloc[0]
    modalidad = df_filtered['Modalidad'].iloc[0]
    st.write(f"**Escuela:** {escuela}")
    st.write(f"**Modalidad:** {modalidad}")

    # Filtrar valores no nulos para gráficos
    df_gramatica = df_filtered[df_filtered['Gramática'].isin(categorias_ordenadas)]
    df_vocabulario = df_filtered[df_filtered['Vocabulario'].isin(categorias_ordenadas)]

    # Contar la frecuencia de estudiantes
    freq_gramatica = df_gramatica['Gramática'].count()
    freq_vocabulario = df_vocabulario['Vocabulario'].count()

    # Gráfico de sectores para Gramática con colores y orden constante
    fig_gramatica = px.pie(df_gramatica, names='Gramática', 
                           category_orders={'Gramática': categorias_ordenadas},
                           color='Gramática')
    fig_gramatica.update_layout(
        title={
            'text': f"Gramática<br><span style='font-size:12px'>Frecuencia: {freq_gramatica} estudiantes",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(t=120)
    )

    # Gráfico de sectores para Vocabulario con colores y orden constante
    fig_vocabulario = px.pie(df_vocabulario, names='Vocabulario', 
                             category_orders={'Vocabulario': categorias_ordenadas},
                             color='Vocabulario')
    fig_vocabulario.update_layout(
        title={
            'text': f"Vocabulario<br><span style='font-size:12px'>Frecuencia: {freq_vocabulario} estudiantes",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(t=120)
    )

    # Crear dos columnas para los gráficos
    col1, col2 = st.columns(2)

    # Mostrar gráfico de Gramática en la primera columna
    col1.plotly_chart(fig_gramatica, use_container_width=True)

    # Mostrar gráfico de Vocabulario en la segunda columna
    col2.plotly_chart(fig_vocabulario, use_container_width=True)

    # Tabla de frecuencias en dos columnas
    st.subheader("Tabla de Frecuencias")
    
    # Crear DataFrames para las tablas con porcentaje (para el PDF)
    tabla_gramatica_pdf = df_filtered['Gramática'].value_counts().reindex(categorias_ordenadas).reset_index()
    tabla_gramatica_pdf.columns = ['Nivel', 'Estudiantes']
    tabla_gramatica_pdf['Porcentaje'] = (tabla_gramatica_pdf['Estudiantes'] / freq_gramatica) * 100
    tabla_gramatica_pdf = tabla_gramatica_pdf.reset_index(drop=True)

    tabla_vocabulario_pdf = df_filtered['Vocabulario'].value_counts().reindex(categorias_ordenadas).reset_index()
    tabla_vocabulario_pdf.columns = ['Nivel', 'Estudiantes']
    tabla_vocabulario_pdf['Porcentaje'] = (tabla_vocabulario_pdf['Estudiantes'] / freq_vocabulario) * 100
    tabla_vocabulario_pdf = tabla_vocabulario_pdf.reset_index(drop=True)

    # Crear DataFrames para las tablas sin porcentaje (para Streamlit)
    tabla_gramatica_visible = tabla_gramatica_pdf[['Nivel', 'Estudiantes']]
    tabla_vocabulario_visible = tabla_vocabulario_pdf[['Nivel', 'Estudiantes']]

    # Crear columnas para las tablas
    col1, col2 = st.columns(2)

    # Mostrar tabla de Gramática en la primera columna
    with col1:
        st.write("**Gramática**")
        st.dataframe(tabla_gramatica_visible)

    # Mostrar tabla de Vocabulario en la segunda columna
    with col2:
        st.write("**Vocabulario**")
        st.dataframe(tabla_vocabulario_visible)

    # Generar PDF
    temp_file_path = "D:\\Phyton\\Pruebas\\PEI-1\\reporte.pdf"
    generar_pdf(escuela, modalidad, tabla_gramatica_pdf, tabla_vocabulario_pdf, temp_file_path, logo_path)
    
    # Proporcionar un enlace para descargar el archivo PDF
    with open(temp_file_path, "rb") as file:
        st.download_button(label="Descargar PDF", data=file, file_name="reporte.pdf", mime="application/pdf")

    # Eliminar el archivo temporal después de la descarga
    os.remove(temp_file_path)

    # Mostrar la leyenda en la página principal
    st.markdown(
        """
        <div style='text-align: center; font-size: 14px; margin-top: 20px;'>
            La información proporcionada en esta página es suministrada por el Centro de Evaluación Educativa del Estado de Yucatán con fines exclusivamente informativos
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.write("CCT no encontrado. Por favor ingresa un CCT válido.")
