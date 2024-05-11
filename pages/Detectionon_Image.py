import calendar
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu


from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import tempfile







hide_st_style = """<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;} </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)




def load_model(model_path):
    model = YOLO(model_path)
    return model

def _display_detected_frames(conf, model, st_frame, image):
    image = cv2.resize(image, (720, int(720 * (9 / 16))))
    res = model.predict(image, conf=conf)
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )

def infer_uploaded_image(conf, model):
    source_img = st.sidebar.file_uploader(
        label="Choose an image...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )

    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            uploaded_image = Image.open(source_img)
            st.image(
                image=uploaded_image,
                caption="Uploaded Image",
                use_column_width=True
            )

    if source_img:
        if st.button("Execution"):
            with st.spinner("Running..."):
                uploaded_image_np = np.array(uploaded_image)
                res = model.predict(uploaded_image_np, conf=conf)
                res_plotted = res[0].plot()[:, :, ::-1]

                with col2:
                    st.image(res_plotted,
                             caption="Detected Image",
                             use_column_width=True)

def infer_uploaded_video(conf, model):
    source_video = st.sidebar.file_uploader(
        label="Choose a video..."
    )

    if source_video:
        st.video(source_video)

    if source_video:
        if st.button("Execution"):
            with st.spinner("Running..."):
                try:
                    tfile = tempfile.NamedTemporaryFile()
                    tfile.write(source_video.read())
                    vid_cap = cv2.VideoCapture(tfile.name)
                    st_frame = st.empty()
                    while (vid_cap.isOpened()):
                        success, image = vid_cap.read()
                        if success:
                            _display_detected_frames(conf, model, st_frame, image)
                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.error(f"Error loading video: {e}")

def main():
    st.title("Early Skin Cancer detection")
    model_path = "/Users/syntichemusawu/Desktop/MidtermProject/best.pt"
    model = load_model(model_path)
    conf = st.sidebar.slider("Confidence", 0.0, 1.0, 0.5)

    task = st.sidebar.radio("Task", ["Image", "Video"])
    if task == "Image":
        infer_uploaded_image(conf, model)
    elif task == "Video":
        infer_uploaded_video(conf, model)

if __name__ == "__main__":
    main()


