import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Setup the environment configuration of API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialization of the model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Define the few-shot prompt with examples
few_shot_prompt = """
You are an intelligent AI. Your task is to provide answers for diet-related questions for specific diseases. 
If a person is suffering from a disease, you need to clarify their doubts and also provide the best foods they need to take.

Example 1:
Q: What foods should I eat if I have diabetes?
A: If you have diabetes, you should focus on eating non-starchy vegetables, lean proteins, whole grains, and healthy fats. Foods such as leafy greens, broccoli, chicken, fish, quinoa, and avocados are good choices. Avoid sugary foods and refined carbs.

Example 2:
Q: What is a good diet for someone with high blood pressure?
A: For high blood pressure, a diet rich in fruits, vegetables, whole grains, and lean proteins is recommended. Foods such as bananas, berries, oats, and fish are beneficial. It's important to reduce salt intake and avoid processed foods.

Example 3:
Q: Can you suggest foods for managing cholesterol levels?
A: To manage cholesterol levels, include foods high in soluble fiber, healthy fats, and omega-3 fatty acids. Oats, beans, nuts, fatty fish like salmon, and olive oil are great options. Avoid trans fats and limit saturated fats.

Please provide dietary advice for the following query:
"""

# Function to get the response
def get_response(few_shot_prompt, question):
    full_prompt = few_shot_prompt + "\nQ: " + question + "\nA:"
    response = chat.send_message(full_prompt, stream=True)
    return response

# Initialization of Streamlit app
st.set_page_config(page_title="Nutrition Helper")

# Add custom CSS for header
st.markdown(
    """
    <style>
    .custom-header {
        font-size: 48px;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Use custom CSS class for header
st.markdown('<div class="custom-header">Nutrition Doctor</div>', unsafe_allow_html=True)

# Checking if there is chat history initiated or not
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Handling the input and submit
input_text = st.text_input("Please input your health-related query for dietary advice.", key="input_text")
submit = st.button("Ask")

if submit and input_text:
    response = get_response(few_shot_prompt, input_text)
    st.session_state['chat_history'].append(("You", input_text))
    st.header("The Response is.....")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Doctorbot", chunk.text))

    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
