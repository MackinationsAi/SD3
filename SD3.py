import streamlit as st
import requests
from PIL import Image
import datetime
import io
import os

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

st.set_page_config(initial_sidebar_state="collapsed", page_icon="static/sai_logo.ico", layout="centered")

def generate_image(api_key, prompt, aspect_ratio, mode, model, seed, output_format, strength=None, negative_prompt=None, image_file=None): #, num_outputs=1):
    headers = {
        "authorization": f"Bearer {api_key}",
        "accept": "image/*"
    }
    data = {
        "prompt": prompt,
        "mode": mode,
        "model": model,
#       "num_outputs": num_outputs,
        "output_format": output_format
    }
    
    files = {"none": ''}  # Default to no file if none provided

    if mode == "text-to-image":
        files["aspect_ratio"] = (None, aspect_ratio)
    elif mode == "image-to-image":
        if seed != 0:
            data['seed'] = seed
    if negative_prompt:
            data['negative_prompt'] = negative_prompt
    if image_file is not None:
            image_bytes = image_file.getvalue()
            files = {'image': ('image.jpg', image_bytes, 'image/jpeg')}
    if strength is not None:
        files["strength"] = (None, str(strength))
    if seed is not None:
        files["seed"] = (None, str(seed))
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers=headers,
        files=files,
        data=data
    )
    return response

def main():
    st.image("static/SD3_webui_logo_image.png", use_column_width=True)
    
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'prompt' not in st.session_state:
        st.session_state.prompt = ""
    if 'negative_prompt' not in st.session_state:
        st.session_state.negative_prompt = ""
    if 'seed' not in st.session_state:
        st.session_state.seed = 0
    
    api_key = st.text_input("Enter your API key:", type="password", value=st.session_state.api_key)
    models = st.selectbox("Select model:", ["sd3", "sd3-turbo"], index=0)
    mode = st.selectbox("Select generation mode:", ["text-to-image", "image-to-image"], index=0)
    prompt = st.text_area("Enter positive prompt:", value=st.session_state.prompt)
    negative_prompt = st.text_input("Enter negative prompt: (optional)", value=st.session_state.negative_prompt)
    aspect_ratios = st.selectbox("Select the aspect ratio:", ["1:1", "2:3", "3:2", "4:5", "5:4", "16:9", "21:9", "9:16", "9:21"], index=0) if mode == "text-to-image" else None
    seed = st.slider("Set seed: (randomize = 0)", min_value=0, max_value=4294967294, value=st.session_state.seed, step=1)
    strength = st.slider("Denoising strength:", min_value=0.0, max_value=1.0, value=0.5, step=0.01) if mode == "image-to-image" else None
#   num_outputs = st.number_input("Batch Count:", min_value=1, max_value=20, value=1, step=1)
    output_formats = st.selectbox("Select the output format:", ["jpeg", "png"], index=1)
    
    st.session_state.api_key = api_key
    st.session_state.prompt = prompt
    st.session_state.negative_prompt = negative_prompt
    st.session_state.seed = seed
    
    uploaded_file = st.file_uploader("Upload for image-to-image generation:", type=["png", "jpg", "jpeg"]) if mode == "image-to-image" else None

    if st.button('Generate Image', use_container_width=True):
        with st.spinner('Generating Image...'):
            result = generate_image(api_key, prompt, aspect_ratios, mode, models, seed, output_formats, strength, negative_prompt, uploaded_file)
            if result.status_code == 200:
                image = Image.open(io.BytesIO(result.content))
                st.image(image, use_column_width=True)
                current_time = datetime.datetime.now().strftime("%Y%m%d_%H.%M.%S").lower()
                file_path = os.path.join(output_dir, f"gen_{models}_{seed}_{current_time}.{output_formats}")
                image.save(file_path)
                st.success(f'Image saved to {file_path}')
            else:
                st.error('Failed to generate image: ' + str(result.json()))
                
    with st.sidebar:
        st.link_button("Stability.Ai _ API Documentation", "https://platform.stability.ai/docs/api-reference")
        with st.expander(("Image Generation Costs"), expanded=True):
            st.markdown((
            """
            - SD3 - 6.5 credits per image or $0.065
            - SD3 Turbo - 4.0 credits per image or $0.04
            
            Additional credits can be purchased via the account_page button below.
            
            Credits cost $10 per 1,000 credits, which is    enough credits for roughly 154 SD3 images or 250 SD3 Turbo images.
            """
        ))
        st.link_button("Account_Page", "https://platform.stability.ai/account/credits")
                
if __name__ == "__main__":
    main()
