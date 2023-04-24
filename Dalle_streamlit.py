import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from IPython import display
import openai
import base64
from datetime import datetime

icon = Image.open("Affine_logo.png")
st.set_page_config(layout="wide", page_title="DALL-E WebApp", page_icon=icon)
st.write("## Inpainting")
st.write("### Try uploading a masked image and a prompt to generate an image that follows your prompt.")
st.sidebar.write("## Upload and download :gear:")

openai.api_key = "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"


def edit_image(image_path, prompt, number, size):
    time_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    image_list = []
    res = openai.Image.create_edit(
        image=open(image_path, "rb"),  # should be square size 'png' image, [RGBA] channel
        #   mask = open(mask_path, "rb"),
        prompt=prompt,
        n=number,
        size=f'{size}x{size}',
        response_format="b64_json"
    )
    for i in range(0, len(res['data'])):
        b64 = res['data'][i]['b64_json']
        filename = f'{prompt[:60]}_{time_str}_{i}.png'
        print('Saving file ' + filename)
        with open(filename, 'wb') as f:
            f.write(base64.urlsafe_b64decode(b64))
        image_list.append(filename)
    print("image_list: ", image_list)
    return image_list


# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def show_upload_image(upload):
    image = Image.open(upload)
    col1.write("Input Image :camera:")
    col1.image(image, "Masked Image with background removed.")


def generate_image(upload, prompt, number_of_images, image_size):

    prompt_list = [prompt]*number_of_images
    with col2:
        st.write("DALL-E prediction :wrench:")
        image_pred = edit_image(upload.name, prompt, number_of_images, image_size)
        print("image prediction: ", image_pred)
        st.image(Image.open(image_pred[0]), prompt)
        # options = st.selectbox(
        #     "Select an image",
        #     ('image{}'.format(i) for i in range(1, number_of_images+1)),
        #     label_visibility="collapsed"
        # )
        # if options == 'image1':
        #     st.image(Image.open(image_pred[0]), prompt)
        # elif options == 'image2':
        #     st.image(Image.open(image_pred[1]), prompt)
        # elif options == 'image3':
        #     st.image(image_pred[2], prompt)
        # elif options == 'image4':
        #     st.image(image_pred[3], prompt)
    #st.sidebar.markdown("\n")
    #st.sidebar.download_button("Download image", , "dalle.png", "image/png")
    return image_pred




col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if my_upload is not None:
    show_upload_image(upload=my_upload)

prompt = st.sidebar.text_area("Prompt", "The item on a table, blue sky, sunny weather, cinematic lighting, 8k resolution.")
num_images = st.sidebar.slider("Number of images", 1, 4, 2)
img_size = st.sidebar.slider("Size of the image", 256, 1024, 1024, step=256)

if "load_state" not in st.session_state:
    st.session_state.load_state = False

if st.sidebar.button("Generate images") or st.session_state.load_state:
    st.session_state.load_state = True
    if my_upload is not None:
        if prompt is not None:
            predictions = generate_image(upload=my_upload, prompt=prompt, number_of_images=num_images, image_size=img_size)
            with col2:
                opt = st.radio("Select image number: ", ['image{}'.format(i) for i in range(1, num_images+1)])
                if opt == 'image1':
                    st.image(Image.open(predictions[0]), prompt)
                elif opt == 'image2':
                    st.image(Image.open(predictions[1]), prompt)
                elif opt == 'image3':
                    st.image(Image.open(predictions[2]), prompt)
        else:
            st.warning("Please write a prompt.", icon="⚠️")
    else:
        st.warning("Please upload an image.", icon="⚠️")
else:
    st.sidebar.write("Please click to generate the images.")

