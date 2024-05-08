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
def get_bot_response(user_input, intents, last_user_input):
    # Here you would implement logic to process the user input and select an appropriate response
    # For simplicity, we'll search for a matching intent and return a random response from its list of responses
    user_input_lower = user_input.lower()
    for intent in intents["intents"]:
        if any(pattern.lower() in user_input_lower for pattern in intent["patterns"]):
            responses = intent["responses"]
            return random.choice(responses)
    
    # Check if the last user input was a question about taking pain relievers
    if last_user_input.lower().startswith("have you taken any pain relievers?"):
        if "no" in user_input_lower:
            return "I understand. If the pain persists, consider consulting a healthcare professional."
        elif "yes" in user_input_lower:
            if "still persist" in user_input_lower:
                return "I'm sorry to hear that. It's advisable to consult a healthcare professional for further evaluation and treatment."
            else:
                return "Good to hear! If you have any questions or concerns, feel free to ask."
    
    # If no matching intent is found and there's no specific follow-up logic, return a default response
    return "I'm sorry, I'm not sure I understand. Can you please provide more details?"

def main():
    st.title("Health Organization Chatbot")
    
    # Load intents from intents.json
    intents = load_intents()

    # Initialize session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "last_user_input" not in st.session_state:
        st.session_state.last_user_input = ""

    # Authenticate the user and get their name
    user_name = authenticate_user()

    # Display welcome message with the user's name
    st.write(f"Welcome, {user_name}!")

    # Display conversation history
    st.subheader("Conversation History")
    for sender, message in st.session_state.conversation_history:
        st.write(f"{sender}: {message}")

    # Add spacing between chat history and input field
    st.write("")

    # Input field for user to enter message
    user_input = st.text_input("Enter your message:", value="", key=f"{user_name}_user_input", placeholder="Enter your message...")

    # Send button
    if st.button("Send") and user_input:
        # Add user's message to the conversation history
        st.session_state.conversation_history.append((user_name, user_input))
        
        # Get bot's response based on user input
        bot_response = get_bot_response(user_input, intents, st.session_state.last_user_input)
        
        # Add bot's response to the conversation history
        st.session_state.conversation_history.append(("Bot", bot_response))

        # Display bot's response
        st.write("Bot:", bot_response)

        # Update last_user_input
        st.session_state.last_user_input = user_input

        # Clear input field after sending message
        user_input = ""

    # Generate QR code section
    st.sidebar.subheader("Scan QR Code to Access Chatbot")
    qr_data = "https://health-organization-chatbot.onrender.com"  # Replace with your Streamlit app URL
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
