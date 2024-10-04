from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-1.5-pro")

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
   
   if uploaded_file is not None:
        
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
            "mime_type": uploaded_file.type,
            "data": bytes_data
            }
        ]
        return image_parts
   else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="multilanguage voice extractor")

st.header("gemini application")
input=st.text_input("input prompt:",key="input")
uploaded_file = st.file_uploader("chosee an image of the ivoice...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

submit =st.button("Tell me about the invoice") 

input_prompt="""
You are an expert in processing high-quality scanned documents. We will upload scanned pages that contain names, addresses, and phone numbers. Your task is to accurately extract only the full name and phone number from each scanned page for our cold-calling campaign. Please ignore any addresses and other irrelevant information.
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    repsonse=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(repsonse)
