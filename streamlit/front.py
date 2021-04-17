import streamlit as st
import requests
import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt
import config
from utils import plot_image
from sound import sound
import speech_recognition as sr
def requestFastAPIEndpoint(image_file,url):
    image = image_file.read()
    file2 = base64.b64encode(image)
    jpg = base64.b64decode(file2)
    jpg_as_np2 = np.frombuffer(jpg, dtype=np.uint8)
    original_image2 = cv2.imdecode(jpg_as_np2, flags=1)
    plt.imshow(cv2.cvtColor(original_image2, cv2.COLOR_BGR2RGB))
    plt.show()
    st.pyplot()
    response = requests.post(url, files={"image_file_read": ("filename", image, "image/jpeg")})
    return response.text

st.title('App')

st.subheader('Detector')

if st.button('Record'):
    with st.spinner(f'Recording for {10} seconds ....'):
        sound.record()
    st.success("Recording completed")
    audio_file = open("recorded.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav')
    r2 = sr.Recognizer()
    with sr.AudioFile("recorded.wav") as source:
        audio2 = r2.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        message=r2.recognize_google(audio2, language="es-ES")
        print("Google Speech Recognition thinks you said " + message)
        st.write(message)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # recognize speech using Sphinx
    try:
        message=r2.recognize_sphinx(audio2, language="es-ESmio")
        print("Sphinx thinks you said " + message)

        st.write(message)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

image_file = st.file_uploader("Upload a file", type=("png","jpg"))

message = st.text_area("pregunta", "")


if st.button('Execute model'):
    st.write(message)
    st.write(f"the url is {config.url['nlp']}")
    responseNLP = requests.post(config.url['nlp'] + message)
    classificacionNLP=eval(responseNLP.text)
    st.write(classificacionNLP)


    if classificacionNLP=="clasificar raza de perro":
        url=config.url['classifyDOGSbreed']
        respuesta=requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)

    elif classificacionNLP=="clasificar raza de gato":
        url=config.url['classify']+'cat_breed'
        # todo train model
        respuesta=requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)

    elif classificacionNLP=="clasificar famoso":
        url=config.url['classify']+'famous'
        # todo train model
        respuesta=requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)

    elif classificacionNLP=="clasificar":
        # todo
        #  añadir endpoint classify general
        url=config.url['classify']+'general'
        respuesta=requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)
#--------------
    elif classificacionNLP=="describir la imagen":
        url = config.url['image_captioning']
        respuesta = requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)
#------------------
    elif classificacionNLP=="contar otros elementos":
        url = config.url['detector']
        respuesta = requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)
        # todo
        #  filtrar contar
#------


    elif classificacionNLP=="contar número de gatos":
        url = config.url['detectorCATS']
        respuesta = requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)
        #todo contar

    elif classificacionNLP=="color del gato":
        url = config.url['detectorCATS']
        respuesta = requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)
        #todo ver color

#--
    elif classificacionNLP=="contar número de perros":
        url = config.url['detectorDOGS']
        respuesta = requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)
        # todo contar

    elif classificacionNLP=="color del perro":
        url = config.url['detectorDOGS']
        respuesta = requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)
        #todo  ver color
#--
    elif classificacionNLP=="contar número de personas":
        url = config.url['detectorPEOPLE']
        respuesta = requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)
        # todo: contar

    elif classificacionNLP=="color prenda":
        url = config.url['detector']
        respuesta = requestFastAPIEndpoint(image_file, url)
        st.write(respuesta)
        # todo
        #  filtrar ropa principal y ver color





    else:
        print(classificacionNLP)


