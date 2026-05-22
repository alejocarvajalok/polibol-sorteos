import streamlit as st
import re
import random

st.set_page_config(
    page_title="Sorteador Polibol",
    page_icon="🎉",
    layout="centered"
)

st.markdown("""
    <style>

    .main {
        background-color: #0e1117;
    }

    .titulo {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: black;
        margin-bottom: 10px;
    }

    .subtitulo {
        text-align: center;
        color: #b0b3b8;
        margin-bottom: 30px;
    }

.ganador-box {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(135deg, #ffb703, #fb8500);
    color: black;
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    line-height: 1.4;
    margin-top: 20px;
    margin-bottom: 20px;
}

    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("LOGO-POLIBOL-WEB.png", width=300)

st.markdown(
    '<div class="titulo">Sorteo Polibol</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Sorteos transparentes para Instagram</div>',
    unsafe_allow_html=True
)

texto = st.text_area(
    "📋 Pegá acá los comentarios copiados desde Instagram",
    height=400,
    placeholder="Pegá aquí los comentarios..."
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

        st.markdown(
    f'''
    <div class="ganador-box">
        🏆 GANADOR <br><br>
        @{ganador}
    </div>
    ''',
    unsafe_allow_html=True
)

        st.info(f"🥈 Suplente 1: @{suplente_1}")

        st.info(f"🥉 Suplente 2: @{suplente_2}")

        st.divider()

        if st.button("🔄 Re-sortear"):

            random.shuffle(usuarios)

            nuevo_ganador = usuarios[0]

            st.warning(f"Nuevo ganador: @{nuevo_ganador}")
