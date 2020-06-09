import streamlit as st
import requests
import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt

st.title('App')

st.subheader('Detector')
image_file = st.file_uploader("Upload a file", type=("png","jpg"))
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
if st.button('Execute model'):
    if image_file is None:
        st.write("load an image")
    else:
        url='http://127.0.0.1:8000/predict'
        response = requests.post(url, files={"image_file_read": ("filename", image_file.read(), "image/jpeg")})
        st.write(response.text)
        