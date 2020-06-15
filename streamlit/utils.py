import cv2
import numpy as np
import matplotlib.pyplot as plt
import base64
import streamlit as st
def plot_image(image_file):
    file = base64.b64encode(image_file.read())
    jpg_original = base64.b64decode(file)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    original_image = cv2.imdecode(jpg_as_np, flags=1)
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    plt.show()
    st.pyplot()