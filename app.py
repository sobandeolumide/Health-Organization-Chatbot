import streamlit as st
import qrcode
from PIL import Image
import io
import json
import random
import time  # Make sure to import the time module


# Function to generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img

# Function to load intents from intents.json
def load_intents():
    try:
        with open("intents.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Intents file not found.")
        return {"intents": []}

# Function to get bot response based on user input
def get_bot_response(user_input, intents, last_user_input):
    user_input_lower = user_input.lower()
    for intent in intents["intents"]:
        if any(pattern.lower() in user_input_lower for pattern in intent["patterns"]):
            responses = intent["responses"]
            return random.choice(responses)
    
    # Check if the last user input was a question about taking pain relievers
    if last_user_input and last_user_input.lower().startswith("have you taken any pain relievers?"):
        if "no" in user_input_lower:
            return "I understand. If the pain persists, consider consulting a healthcare professional. 😔"
        elif "yes" in user_input_lower:
            if "still persist" in user_input_lower:
                return "I'm sorry to hear that. It's advisable to consult a healthcare professional for further evaluation and treatment. 😟"
            else:
                return "Good to hear! If you have any questions or concerns, feel free to ask. 😌"
    
    # If no matching intent is found and there's no specific follow-up logic, return a default response
    return "I'm sorry, I'm not sure I understand. Can you please provide more details? 🤔"

def display_chat_message(role, content):
    if role == "user":
        avatar = "👨"  # Using a human emoji for the user avatar
    else:
        avatar = "🤖"
    
    # Custom HTML for displaying the message with emoji avatar outside the box
    st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 10px;'>
        <div style='width: 36px; height: 36px; border-radius: 50%; background-color: #f2f2f2; display: flex; justify-content: center; align-items: center; font-size: 18px; margin-right: 10px;'>
            {avatar}
        </div>
        <div style='padding: 10px; background-color: {"#ffefef" if role == "user" else "#f9f9f9"}; border-radius: 5px;'>
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.title("Health Organization Chatbot")
    
    # Load intents from intents.json
    intents = load_intents()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])

    # React to user input
    prompt = st.chat_input("What's up?")
    if prompt: 
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt)

        # Get the last message for context
        last_user_input = st.session_state.messages[-2]["content"] if len(st.session_state.messages) > 1 else ""

        # Add a delay of 5 seconds before bot responds
        time.sleep(1)
        
        # Get bot response
        bot_response = get_bot_response(prompt, intents, last_user_input)

        # Display bot response in chat message container
        display_chat_message("bot", bot_response)
        # Add bot message to chat history
        st.session_state.messages.append({"role": "bot", "content": bot_response})

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
    
    

