import streamlit as st 
import pandas as pd    #LIBRERIA DE PANDAS PARA MANEJO DE EXCEL
from PIL import Image  
import base64          #LIBRERIA PARA TRABAJAR CON LOS FONDOS
from Levenshtein import ratio
#Hola MUNDO: Iremos paso por paso en la creación de esta app:

####1 ER PASO: Debemos extraer las tablas de datos de nuestra hoja EXCEL 'mapudungun.xlsx'
#TABLA PARA CONSONANTE:
datos_kon=pd.read_excel('mapudungun.xlsx',sheet_name='kon')
#TABLA PARA TERMINACIÓN EN 'AEOU':
datos_tripa=pd.read_excel('mapudungun.xlsx',sheet_name='tripa')
#TABLA PARA TERMINACIÓN EN 'I':
datos_pi=pd.read_excel('mapudungun.xlsx',sheet_name='pi')
####2 DO PASO: Ahora debemos crear diccionarios para poder acceder a cada una de las combinaciones, en este caso tomaremos la columna
####'persona' como índice
#CREANDO DICCIONARIO PARA TERMINACIÓN EN CONSONANTE:
D_kon=datos_kon.set_index('persona').to_dict(orient='index')
#CREANDO DICCIONARIO PARA TERMINACIÓN EN 'AEOU':
D_tripa=datos_tripa.set_index('persona').to_dict(orient='index')
#CREANDO DICCIONARIO PARA TERMINACIÓN EN 'I':
D_pi=datos_pi.set_index('persona').to_dict(orient='index')
#3 ER PASO: 
#st.title("¡Bienvenidos al conjugador de verbos en Mapudungun! :smile:")
import streamlit as st

st.markdown('<h1 style="color: black;">Conjugador de verbos en Mapudungun</h1>', unsafe_allow_html=True)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('fondo.jpg')    

import streamlit as st

import streamlit as st

texto = """
El mapudungun es una lengua hablada por el pueblo mapuche. Es una lengua rica y fascinante que refleja su grandiosa cultura y cosmovisión.

En el mapudungun, los verbos se conjugan en diferentes formas. Veamos algunos ejemplos de conjugación en modo indicativo del verbo "am" que significa "hablar":

- Singular:
  - Amu: Yo hablo
  - Amulei: Tú hablas
  - Amuwe: Él/Ella habla

- Dual:
  - Amutu: Nosotros dos hablamos
  - Amuleiñ: Ustedes dos hablan
  - Amutulei: Ellos/Ellas dos hablan

- Plural:
  - Amulen: Nosotros hablamos
  - Amuleiñ: Ustedes hablan
  - Amulen: Ellos/Ellas hablan

Estos ejemplos ilustran cómo los verbos en mapudungun se conjugan de acuerdo a las personas gramaticales (primera, segunda y tercera) y al número (singular, dual y plural). La conjugación de los verbos en mapudungun es una característica importante de esta hermosa lengua.

Explora más sobre la lengua mapudungun y disfruta de su riqueza cultural y lingüística.

¡Bienvenidos al mundo del mapudungun! :smile:
"""

st.markdown(f'<p style="color: black;">{texto}</p>', unsafe_allow_html=True)

####5 TO PASO: LÓGICA DEL PROGRAMA



def mostrar_verbos():
    verbos = {
        "am-": "hablar",
        "pewk-": "cantar",
        "melih-": "correr",
        "w-": "ver",
        "ley-": "dormir",
        "kutx-": "comer",
        "ray-": "andar",
        "pay-": "ir",
        "metx-": "escuchar",
        "ruk-": "entrar",
        "lawen-": "amar",
        "ralün-": "caminar",
        "eymi-": "sentir",
        "kaxo-": "caer",
        "fe-": "hacer",
        "welu-": "existir",
        "lafken-": "nadar",
        "kisu-": "saber",
        "anum-": "construir",
        "trawün-": "pensar"
    }

    st.write("**Aquí te dejo algunos verbos en Mapudungun y su traducción al español :**")

    for verbo, traduccion in verbos.items():
        st.write(f"- {verbo}: {traduccion}")

def conjugar_verbo(palabra,persona,numero):
    if palabra== '': 
        palabra='hola'
    else:
        palabra=palabra
    ultima_letra=palabra[-1]
    if ultima_letra not in 'aeiou':
        palabra_transformada=palabra+' '+D_kon[persona][numero]
    elif ultima_letra in "aeou":
        palabra_transformada=palabra+' '+D_tripa[persona][numero]
    elif ultima_letra == 'i':
        palabra_transformada=palabra+' '+D_pi[persona][numero]
    return palabra_transformada

def generador_conjugaciones(palabra,palabra_conjugada):
    diccionario_principal = {}
    valor_maximo=0
    pers=1
    num="singular"
    for i in [1,2,3]:
        diccionario_secundario = {}
        for j in ["singular","dual","plural"]:
            valor = conjugar_verbo(palabra,i,j)  # Puedes establecer cualquier valor que desees
            diccionario_secundario[j] = valor
            valor_ratio=ratio(valor,palabra_conjugada)
            if valor_ratio>valor_maximo:
                valor_maximo=valor_ratio
                pers=i
                num=j
        diccionario_principal[i] = diccionario_secundario
    resultado=[diccionario_principal,valor_maximo,pers,num]
    return resultado

palabra=st.selectbox('Elige un verbo a conjugar', ['am', 'pewk','melih','w','ley','kutx','ray','pay','metx','ruk','lawen','ralün','eymi','kaxo','fe','welu','lafken','kisu','anum','trawün'])
numero_adivinar=st.selectbox("Selecciona una persona gramatical", ["singular","dual","plural"])
persona_adivinar=st.selectbox("Selecciona un número gramatical",[1,2,3])
import streamlit as st

texto_negrita = "Ahora te toca a ti probar cómo vas con las conjugaciones en esta lengua. Aquí te dejo una opción divertida para que sigas aprendiendo. Deberás escoger un verbo y luego escribir su conjugación, y nosotros te diremos la conjugación correcta, así como el número y la persona gramatical que tiene tu conjugación. ¡Suerte!"

st.markdown(f"**{texto_negrita}**")

palabra_conjugada=st.text_input(label="Ingresa un verbo conjugado")

mostrar_verbos()
if st.button('Conjugar'):
    resultado_conjugacion=generador_conjugaciones(palabra,palabra_conjugada)
    diccionario=resultado_conjugacion[0]
    ratio_max=resultado_conjugacion[1]
    persona_conjugacion=resultado_conjugacion[2]
    numero_conjugacion=resultado_conjugacion[3]
    palabra_conjugacion=diccionario[persona_conjugacion][numero_conjugacion]
    palabra_adivinar=conjugar_verbo(palabra,persona_adivinar,numero_adivinar)
    if palabra_conjugacion==palabra_adivinar:
        st.write("¡Bien hecho, la palabra ingresada corresponde a la conjugación seleccionada")
        st.write("Con la persona:",persona_conjugacion)
        st.write("Y número de conjugación:",numero_conjugacion)
        st.write("Palabra conjugada:",palabra_conjugacion)
    else:
        st.write("Lo lamentamos, la palabra que ingresaste no es correcta, debería ser:",palabra_adivinar)
        st.write("La que ingresaste tiene persona:",persona_conjugacion)
        st.write("Y número de conjugación:",numero_conjugacion)
        st.write("Palabra conjugada:",palabra_conjugacion)
        

import streamlit as st

def mostrar_mensaje_final():
    mensaje = """
        <div style="text-align: center; font-size: 18px; color: #333333;">
            <p>Gracias por visitarnos. Seguiremos trabajando para contribuir con el aprendizaje y la difusión de más lenguas valiosas.</p>
        </div>
    """
    st.markdown(mensaje, unsafe_allow_html=True)



# Al final de tu aplicación, después de mostrar los resultados
mostrar_mensaje_final()

        
        
        