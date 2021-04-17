import streamlit as st
import requests
import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt
import config
from utils import plot_image

st.title('App')

st.subheader('Detector')
image_file = st.file_uploader("Upload a file", type=("png","jpg"))

message = st.text_area("pregunta", "")

if st.button('Plot image'):
    if image_file is None:
        st.write("load a image")
    else:
        file = base64.b64encode(image_file.read())
        jpg_original = base64.b64decode(file)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        original_image = cv2.imdecode(jpg_as_np, flags=1)
        plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        plt.show()
        st.pyplot()

action = st.radio("What do you want to do",('NLP','detect', 'classify dog breed', 'classify cat breed',
                                           'classify famous face', 'image captioning'))
if action == 'NLP':
    url = config.url['nlp']
    st.write('You selected nlp.')

elif action == 'detect':
    url = config.url['detector']
    st.write('You selected detect.')

elif action == 'classify dog breed':
    url = config.url['classify']+'dog_breed'
    st.write("You  select classify dog breed.")

elif action == 'classify cat breed':
    url = config.url['classify']+'cat_breed'
    st.write("You select classify cat breed.")

elif action == 'classify famous face':
    url = config.url['classify']+'famous'
    st.write("You select classify famous face.")

elif action == 'image captioning':
    url = config.url['image_captioning']
    st.write("You select image captioning.")
else:
    st.write("This option is not ready yet")

if st.button('Execute model'):

    if action == 'NLP':
        st.write(message)
        st.write(f"the url is {url}")
        response = requests.post(url+message)
        st.write(response.text)

    else:
        if image_file is None:
            st.write("load an image")
        else:
            #url='http://127.0.0.1:8000/predict'
            st.write(f"the url is {url}")
            image=image_file.read()
            file2 = base64.b64encode(image)
            jpg = base64.b64decode(file2)
            jpg_as_np2 = np.frombuffer(jpg, dtype=np.uint8)
            original_image2 = cv2.imdecode(jpg_as_np2, flags=1)
            plt.imshow(cv2.cvtColor(original_image2, cv2.COLOR_BGR2RGB))
            plt.show()
            st.pyplot()

            response = requests.post(url, files={"image_file_read": ("filename", image, "image/jpeg")})
            st.write(response.text)
