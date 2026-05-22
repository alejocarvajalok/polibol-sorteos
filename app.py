import streamlit as st
import re
import random

st.set_page_config(
    page_title="Sorteador Polibol",
    layout="centered"
)

st.title("🎉 Sorteador de Instagram - Polibol")

st.markdown("Pegá los comentarios copiados directamente desde Instagram.")

texto = st.text_area(
    "Comentarios",
    height=400
)

def limpiar_comentarios(texto):

    lineas = [l.strip() for l in texto.split("\n") if l.strip()]

    participantes = {}
    invalidos = []

    i = 0

    while i < len(lineas):

        linea = lineas[i]

        # Detectar inicio bloque comentario
        if linea.startswith("Foto del perfil de"):

            # Extraer username REAL
            usuario = linea.replace("Foto del perfil de", "").strip()

            comentario = ""

            # Buscar comentario real
            for j in range(i + 1, min(i + 8, len(lineas))):

                posible = lineas[j]

                # Ignorar timestamps
                if re.match(r'^\d+\s?(h|min|d)$', posible):
                    continue

                # Ignorar líneas basura
                if posible in [
                    "Responder",
                    "Editado"
                ]:
                    continue

                # Ignorar username repetido
                if posible == usuario:
                    continue

                comentario = posible
                break

            menciones = re.findall(r'@\w+', comentario)

            # Texto SIN menciones
            texto_limpio = re.sub(r'@\w+', '', comentario).strip()

            # VALIDACIONES

            if len(menciones) < 2:

                invalidos.append(
                    f"❌ @{usuario} → menos de 2 menciones"
                )

            elif len(texto_limpio) < 3:

                invalidos.append(
                    f"❌ @{usuario} → no comentó figurita"
                )

            else:

                if usuario not in participantes:

                    participantes[usuario] = comentario

        i += 1

    return participantes, invalidos

if st.button("Procesar comentarios"):

    participantes, invalidos = limpiar_comentarios(texto)

    st.subheader("✅ Participantes válidos")

    for usuario, comentario in participantes.items():

        st.write(f"@{usuario} → {comentario}")

    st.success(f"Total válidos: {len(participantes)}")

    st.divider()

    st.subheader("❌ Comentarios inválidos")

    if len(invalidos) == 0:

        st.info("No se encontraron inválidos.")

    else:

        for invalido in invalidos:

            st.write(invalido)

    st.divider()

    if len(participantes) >= 1:

        usuarios = list(participantes.keys())

        random.shuffle(usuarios)

        ganador = usuarios[0]

        suplente_1 = usuarios[1] if len(usuarios) > 1 else "No disponible"
        suplente_2 = usuarios[2] if len(usuarios) > 2 else "No disponible"

        st.subheader("🏆 Resultado del Sorteo")

        st.balloons()

        st.success(f"🥇 Ganador: @{ganador}")

        st.info(f"🥈 Suplente 1: @{suplente_1}")

        st.info(f"🥉 Suplente 2: @{suplente_2}")

        st.divider()

        if st.button("🔄 Re-sortear"):

            random.shuffle(usuarios)

            nuevo_ganador = usuarios[0]

            st.warning(f"Nuevo ganador: @{nuevo_ganador}")
```
