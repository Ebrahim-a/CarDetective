import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

genai.configure(api_key=api_key)

# Set up the model
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

#safety setting

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]


model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
])

system_prompt="""
Detect which car is this picture

Your Responsibilities include:

1. Document what car do you see
2. What Brand is the car
3. What year of making is the car
4. Price of the car

"""

convo.send_message("YOUR_USER_INPUT")
print(convo.last.text)



# set pag config

st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

#set title
st.title("Car Finder")
st.subheader("An Application that can help user identify Cars")
uploaded_file = st.file_uploader("Upload the image", type=["png","jpg","jpeg"])
submit_button = st.button("Generate")

if submit_button:
    image_data = uploaded_file.getvalue()

    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]

    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]

    response = model.generate_content(prompt_parts)
    st.write(response.text)
