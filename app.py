import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model configuration
generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config
)

# Initialize chat session with initial history
initial_history = [
    {
        "role": "user",
        "parts": ["Pretend you are an expert in generating marketing content or blog for products and services offered by any company.\
      You just need the url link of that company's website from the user to collect information and learn about the company.\
      You can handle modify the content based on the user feedback. If queries are ambiguous then you ask for more details.\
      You don't know about anything else in the world, so you refrain from responding to any other type of queries.",
        ],
    },
    {
        "role": "model",
        "parts": [
            "Please provide me with the URL of the company's website so I can generate a compelling marketing blog post for their products and services.  \n\nOnce I have the URL, I will:\n\n* **Analyze the website:** I will examine the content, products, and services offered to understand the company's target audience and value proposition. \n* **Craft an original and engaging headline:** I will create a headline that is relevant, attention-grabbing, and accurately reflects the blog post's content.\n* **Develop a compelling narrative:** I will write a blog post that is informative, engaging, and showcases the benefits of using the company's products and services. \n* **Include relevant keywords:**  I will use keywords that are likely to be used by potential customers searching for the company's products and services online.\n* **Format the content for readability:** The content will be easy to read and understand, with clear headings, subheadings, and bullet points.\n\nI'm excited to help you create a blog post that will attract new customers and drive business growth! \n",
        ],
    },
]

# Streamlit app setup
st.title(":pencil: Marketing Content Generator")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = initial_history
    st.session_state['display_history'] = []

# Initialize temporary input storage
if 'temp_input' not in st.session_state:
    st.session_state['temp_input'] = ""

# Function to handle user input and model response
def generate_response(user_input):
    # Add the user input to the chat history
    st.session_state['chat_history'].append({"role": "user", "parts": [user_input]})

    # Send the entire chat history to the model to generate a response
    chat_session = model.start_chat(history=st.session_state['chat_history'])
    response = chat_session.send_message(user_input)

    # Add the model's response to the chat history
    st.session_state['chat_history'].append({"role": "model", "parts": [response.text]})
    return response.text

# Display chat history
if st.session_state['display_history']:
    for chat in st.session_state['display_history']:
        st.write(chat)

# Input field for user queries
user_input = st.text_input("Enter your query:", value=st.session_state['temp_input'])

# Generate button
if st.button("Generate"):
    if user_input.strip():
        st.session_state['display_history'].append(f"You: {user_input}")
        response_text = generate_response(user_input)
        st.session_state['display_history'].append(f"Bot: {response_text}")
        st.session_state['temp_input'] = ""  # Clear the temporary input
        st.rerun()
        
# Update temporary input storage
st.session_state['temp_input'] = " "
