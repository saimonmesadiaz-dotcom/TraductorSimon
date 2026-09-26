import streamlit as st
import os
import time
import glob

from bokeh.models import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

from gtts import gTTS
from googletrans import Translator


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Traductor",
    layout="centered"
)


# =========================================================
# FONDO
# =========================================================

st.markdown("""
<style>

.stApp {
    background-image:
        linear-gradient(
            rgba(0, 0, 0, 0.55),
            rgba(0, 0, 0, 0.55)
        ),
        url("idiomas.JPG");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}


/* Contenedor principal */

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}


/* Título */

h1 {
    text-align: center;
}


/* Botón */

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}


/* Selectores */

div[data-baseweb="select"] > div {
    border-radius: 10px;
}


/* Imagen centrada */

[data-testid="stImage"] {
    display: flex;
    justify-content: center;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CARPETA TEMPORAL
# =========================================================

try:
    os.mkdir("temp")
except:
    pass


# =========================================================
# TÍTULO
# =========================================================

st.title("TRADUCTOR.")


# =========================================================
# IMAGEN ORIGINAL
# =========================================================

# DEJA AQUÍ EL MISMO NOMBRE DE LA IMAGEN
# QUE TENÍAS EN TU CÓDIGO ORIGINAL.

st.image(
    "Imagen Traduccion y Reconocimiento.png",
    width=500
)


# =========================================================
# SUBTÍTULO
# =========================================================

st.subheader("Escucho lo que quieres traducir.")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.subheader("Traductor.")

    st.write(
        "Presiona el botón, cuando escuches la señal "
        "habla lo que quieres traducir, luego selecciona "
        "la configuración de lenguaje que necesites."
    )


# =========================================================
# RECONOCIMIENTO DE VOZ
# =========================================================

st.write(
    "Toca el Botón y habla lo que quieres traducir"
)


stt_button = Button(
    label="Escuchar",
    width=300,
    height=50
)


stt_button.js_on_event(
    "button_click",
    CustomJS(code="""

        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'es-ES';

        recognition.onresult = function(e) {

            var value = "";

            for (
                var i = e.resultIndex;
                i < e.results.length;
                ++i
            ) {

                if (e.results[i].isFinal) {

                    value += e.results[i][0].transcript;

                }

            }

            if (value != "") {

                document.dispatchEvent(
                    new CustomEvent(
                        "GET_TEXT",
                        {detail: value}
                    )
                );

            }

        };

        recognition.onend = function() {

            console.log(
                "Reconocimiento detenido"
            );

        };

        recognition.start();

    """)
)


result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)


# =========================================================
# TRADUCCIÓN
# =========================================================

if result:

    if "GET_TEXT" in result:

        text = str(
            result.get("GET_TEXT")
        )


        # =================================================
        # TEXTO RECONOCIDO
        # =================================================

        st.subheader(
            "Texto reconocido"
        )

        st.write(text)


        translator = Translator()


        # =================================================
        # COLUMNAS
        # =================================================

        col1, col2 = st.columns(2)


        # =================================================
        # IDIOMA DE ENTRADA
        # =================================================

        with col1:

            in_lang = st.selectbox(
                "Lenguaje de entrada",
                (
                    "Inglés",
                    "Español",
                    "Italiano",
                    "Frances",
                    "Aleman",
                    "Checo",
                    "Coreano",
                    "Mandarín",
                    "Japonés"
                )
            )


        # =================================================
        # IDIOMAS
        # =================================================

        idiomas = {

            "Inglés": "en",
            "Español": "es",
            "Italiano": "it",
            "Frances": "fr",
            "Aleman": "de",
            "Checo": "cs",
            "Coreano": "ko",
            "Mandarín": "zh-cn",
            "Japonés": "ja"

        }


        input_language = idiomas[in_lang]


        # =================================================
        # IDIOMA DE SALIDA
        # =================================================

        with col2:

            out_lang = st.selectbox(
                "Lenguaje de salida",
                (
                    "Inglés",
                    "Español",
                    "Italiano",
                    "Frances",
                    "Aleman",
                    "Checo",
                    "Coreano",
                    "Mandarín",
                    "Japonés"
                )
            )


        output_language = idiomas[out_lang]


        # =================================================
        # ACENTO
        # =================================================

        english_accent = st.selectbox(
            "Selecciona el acento",
            (
                "Defecto",
                "Español",
                "Reino Unido",
                "Estados Unidos",
                "Canada",
                "Australia",
                "Irlanda",
                "Sudáfrica"
            )
        )


        acentos = {

            "Defecto": "com",
            "Español": "com.mx",
            "Reino Unido": "co.uk",
            "Estados Unidos": "com",
            "Canada": "ca",
            "Australia": "com.au",
            "Irlanda": "ie",
            "Sudáfrica": "co.za"

        }


        tld = acentos[english_accent]


        # =================================================
        # TEXTO A AUDIO
        # =================================================

        def text_to_speech(
            input_language,
            output_language,
            text,
            tld
        ):

            translation = translator.translate(
                text,
                src=input_language,
                dest=output_language
            )


            trans_text = translation.text


            tts = gTTS(
                trans_text,
                lang=output_language,
                tld=tld,
                slow=False
            )


            my_file_name = text[:20]


            my_file_name = "".join(
                c
                for c in my_file_name
                if c.isalnum()
                or c in (" ", "_", "-")
            )


            if not my_file_name:

                my_file_name = "audio"


            tts.save(
                f"temp/{my_file_name}.mp3"
            )


            return (
                my_file_name,
                trans_text
            )


        # =================================================
        # MOSTRAR TEXTO
        # =================================================

        display_output_text = st.checkbox(
            "Mostrar el texto traducido"
        )


        # =================================================
        # CONVERTIR
        # =================================================

        if st.button("Convertir"):

            result_file, output_text = text_to_speech(
                input_language,
                output_language,
                text,
                tld
            )


            audio_file = open(
                f"temp/{result_file}.mp3",
                "rb"
            )


            audio_bytes = audio_file.read()


            st.subheader(
                "Tu audio"
            )


            st.audio(
                audio_bytes,
                format="audio/mp3",
                start_time=0
            )


            if display_output_text:

                st.subheader(
                    "Texto de salida"
                )

                st.write(
                    output_text
                )


        # =================================================
        # LIMPIAR ARCHIVOS
        # =================================================

        def remove_files(n):

            mp3_files = glob.glob(
                "temp/*mp3"
            )


            if len(mp3_files) != 0:

                now = time.time()

                n_days = n * 86400


                for f in mp3_files:

                    if os.stat(f).st_mtime < now - n_days:

                        os.remove(f)


        remove_files(7)


