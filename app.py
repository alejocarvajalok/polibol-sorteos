import streamlit as st
import re
import random

st.set_page_config(page_title="Sorteador Polibol")

st.title("🎉 Sorteador de Instagram - Polibol")

texto = st.text_area(
    "Pegá acá los comentarios copiados desde Instagram",
    height=400
)

def limpiar_comentarios(texto):

    lineas = [l.strip() for l in texto.split("\n") if l.strip()]

    participantes = {}

    i = 0

    while i < len(lineas):

        linea = lineas[i]

        # Detectar inicio de comentario
        if linea.startswith("Foto del perfil de"):

            # Username debería estar 1 línea abajo
            if i + 1 < len(lineas):

                usuario = lineas[i + 1]

                comentario = ""

                # Buscar comentario real en próximas líneas
                for j in range(i + 2, min(i + 6, len(lineas))):

                    posible = lineas[j]

                    # Ignorar timestamps
                    if re.match(r'^\d+\s?(h|min|d)$', posible):
                        continue

                    # Ignorar líneas basura
                    if posible in ["Responder", "Editado"]:
                        continue

                    comentario = posible
                    break

                menciones = re.findall(r'@\w+', comentario)

                # Validar mínimo 2 menciones
                if len(menciones) >= 2:

                    # Evitar duplicados
                    if usuario not in participantes:

                        participantes[usuario] = comentario

        i += 1

    return participantes

if st.button("Procesar comentarios"):

    participantes = limpiar_comentarios(texto)

    st.subheader("✅ Participantes válidos")

    for usuario, comentario in participantes.items():

        st.write(f"@{usuario} → {comentario}")

    st.success(f"Total válidos: {len(participantes)}")

    if len(participantes) > 0:

        ganador = random.choice(list(participantes.keys()))

        st.subheader("🏆 Ganador")

        st.balloons()

        st.success(f"🎉 @{ganador}")
