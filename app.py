import streamlit as st
#from openai import OpenAI

from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_community.document_transformers import MarkdownifyTransformer
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
import streamlit.components.v1 as components

import re
from bs4 import BeautifulSoup

import os
import yaml


def get_prompt(area_academica, asignatura, rango_edad, meta):
    prompt_template = f"""
Debes generar un listado de 10 posibles temáticas para un curso 
en el área académica: {area_academica}, para la asignatura {asignatura},
para alumnos con edad en el rango de {rango_edad}, y la meta de aprendizaje es
la siguiente: {meta}

Respuesta:\n

"""
    prompt = PromptTemplate.from_template(prompt_template)

    return prompt


def get_temas_chain(prompt, llm):
    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return chain





@st.dialog("¿Cómo obtengo la clave API?",width="large")
def tutorial():
    components.iframe("https://drive.google.com/file/d/1736upJlBXJAw6OFPhwNo8z298XMuN-_J/preview", 
                      width=720, height=420, )


with st.sidebar:
    st.markdown("Para poder usar el chatbot deberás obtener una clave API de Google Gemini y agregarla debajo:")
    gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    if st.button("¿Cómo obtengo la clave API 🤔?"):
        tutorial()
    "[Obtener clave API para Gemini](https://ai.google.dev/gemini-api?hl=es-419)"

    st.divider()
    st.markdown("Desarrollado por: *Lic. Illak Zapata*")

    columns = st.sidebar.columns(6)

    with columns[1]:
        st.write("""<div style="width:100%;text-align:center;"><a href="https://www.linkedin.com/in/illakzapata/" style="float:center"><img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="22px"></img></a></div>""", unsafe_allow_html=True)

    with columns[2]:
        st.write("""<div style="width:100%;text-align:center;"><a href="https://github.com/illak" style="float:center"><img src="https://img.icons8.com/material-outlined/48/000000/github.png" width="22px"></img></a></div>""", unsafe_allow_html=True)

    with columns[3]:
        st.write("""<div style="width:100%;text-align:center;"><a href="https://illak-blog.netlify.app/" style="float:center"><img src="https://www.freeiconspng.com/uploads/website-icon-11.png" width="22px"></img></a></div>""", unsafe_allow_html=True)


st.title("Crea tu curso - prueba")

area_academica = st.selectbox(
    "Seleccione el área académica",
    ("Tecnología e Informática","Matemáticas"),
    index=None,
    placeholder="Seleccione una opción..."
)

if area_academica:
    match area_academica:
        case "Tecnología e Informática":
            asignatura = st.selectbox(
                "Seleccione asignatura",
                ("Informática","Pensamiento computacional", "Tecnología"),
                index=None,
                placeholder="Seleccione una opción..."
            )
        case "Matemáticas":
            asignatura = st.selectbox(
                "Seleccione asignatura",
                ("Algebra","Arítmetica","Cálculo","Estadística y Probabilidad","Geometría"),
                index=None,
                placeholder="Seleccione una opción..."
            )

rango_edad = st.radio(
    "Seleccione el rango etario de sus estudiantes:",
    ["5-6", "7-8", "9-10","11-12","13-14","15-16","17+"],
    index=None,
)

meta = st.text_input("Finalmente, indique las metas o propósitos de aprendizaje")

if st.button("Definir temas del curso") and gemini_api_key:
    if area_academica and asignatura and rango_edad and meta:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_api_key)
    
        prompt = get_prompt(area_academica, asignatura, rango_edad, meta)
        temas_chain = get_temas_chain(prompt, llm)
        
        with st.spinner('Estoy procesando los datos y generando posibles temas... aguarde por favor.'):
            response = temas_chain.invoke({})
            st.markdown(response)

        print(response)
    else:
        st.error("Todos los campos anteriores son obligatorios!!")

if not gemini_api_key:
    st.info("Por favor agregue su clave API de Google Gemini.")
    st.stop()