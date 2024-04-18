import streamlit as st
import os
from PIL import Image
import glob

output_dir = "outputs"
st.set_page_config(initial_sidebar_state="expanded", page_icon="static/sai_logo.ico", layout="centered")

with st.sidebar:
   st.link_button("Stability.Ai _ API Documentation", "https://platform.stability.ai/docs/api-reference")
   with st.expander(("Image Generation Costs"), expanded=True):
            st.markdown((
            """
            - SD3 - 6.5 credits per image or $0.065
            - SD3 Turbo - 4.0 credits per image or $0.04
            
            Additional credits can be purchased via the account_page button below.
            
            Credits cost $10 per 1,000 credits, which is enough credits for roughly 154 SD3 images or 250 SD3 Turbo images.
            """
      ))
   st.link_button("Account_Page", "https://platform.stability.ai/account/credits")
files = glob.glob(os.path.join(output_dir, '*'))
for file in files:
   image = Image.open(file)
   st.image(image, caption=os.path.basename(file), use_column_width=True)