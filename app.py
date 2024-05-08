import streamlit as st
import qrcode
from PIL import Image
import io
import json
import random

# Function to authenticate the user and get their name
def authenticate_user():
    st.sidebar.title("Sign In")
    user_name = st.sidebar.text_input("Enter your name:", "")
    return user_name

# Function to generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img

# Function to load intents from intents.json
def load_intents():
    with open("intents.json", "r") as file:
        return json.load(file)

# Function to get bot response based on user input
def get_bot_response(user_input, intents):
    # Here you would implement logic to process the user input and select an appropriate response
    # For simplicity, we'll search for a matching intent and return a random response from its list of responses
    user_input_lower = user_input.lower()
    for intent in intents["intents"]:
        if any(pattern.lower() in user_input_lower for pattern in intent["patterns"]):
            responses = intent["responses"]
            return random.choice(responses)
    # If no matching intent is found, return a default response
    return "I'm sorry, I don't understand that."

def main():
    st.title("Health Organization Chatbot")
    
    # Load intents from intents.json
    intents = load_intents()

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Authenticate the user and get their name
    user_name = authenticate_user()

    # Display welcome message with the user's name
    st.write(f"Welcome, {user_name}!")

    # List to store conversation history
    conversation_history = st.session_state.chat_history

    # Display conversation history
    st.subheader("Conversation History")
    for sender, message in conversation_history:
        st.write(f"{sender}: {message}")

    # Add spacing between chat history and input field
    st.write("")

    # Create a container for input field and button
    input_container = st.container()

    # Input field for user to enter message
    with input_container:
        user_input = st.text_input("Enter your message:", value="", key=f"{user_name}_user_input", placeholder="Enter your message...")

    # Send button
    with input_container:
        if st.button("Send") and user_input:
            # Add user's message to the conversation history
            conversation_history.append((user_name, user_input))
            
            # Get bot's response based on user input
            bot_response = get_bot_response(user_input, intents)
            
            # Add bot's response to the conversation history
            conversation_history.append(("Bot", bot_response))

            # Clear input field after sending message
            user_input = ""

    # Update session state
    st.session_state.chat_history = conversation_history

    # Generate QR code section
    st.sidebar.subheader("Scan QR Code to Access Chatbot")
    qr_data = "https://http://localhost:8501/"  # Replace with your Streamlit app URL
    qr_code = generate_qr_code(qr_data)
    
    # Convert QR code image to bytes
    img_byte_array = io.BytesIO()
    qr_code.save(img_byte_array, format='PNG')
    qr_image_bytes = img_byte_array.getvalue()
    
    # Display QR code image
    st.sidebar.image(qr_image_bytes, use_column_width=True)

# Call the main function
if __name__ == "__main__":
    main()
