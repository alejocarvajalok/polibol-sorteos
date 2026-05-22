import streamlit as st
import re
import random

st.set_page_config(page_title="Sorteador Polibol")

st.title("🎉 Sorteador de Instagram - Polibol")

texto = st.text_area(
    "Pegá acá los comentarios copiados desde Instagram",
    height=300
)

def limpiar_comentarios(texto):
    lineas = texto.split("\n")

    participantes = {}

    i = 0

    while i < len(lineas):

        linea = lineas[i].strip()

        # Detectar posible username
        if (
            linea
            and " " not in linea
            and not linea.endswith("h")
            and "Foto del perfil" not in linea
            and "Responder" not in linea
            and "Me gusta" not in linea
        ):

            usuario = linea

            comentario = ""

            if i + 1 < len(lineas):
                comentario = lineas[i + 1]

            menciones = re.findall(r'@\w+', comentario)

            if len(menciones) >= 2:

                if usuario not in participantes:
                    participantes[usuario] = comentario

        i += 1

    return participantes

if st.button("Procesar comentarios"):

    participantes = limpiar_comentarios(texto)

    st.subheader("✅ Participantes válidos")

    for usuario in participantes:
        st.write(f"@{usuario}")

    st.success(f"Total válidos: {len(participantes)}")

    if len(participantes) > 0:

        ganador = random.choice(list(participantes.keys()))

        st.subheader("🏆 Ganador")

        st.balloons()

        st.success(f"🎉 @{ganador}")
