import streamlit as st
import qrcode
from PIL import Image
import io
import json
import random


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
        with open("intents.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Intents file not found.")
        return {"intents": []}

# Function to get bot response based on user input
def get_bot_response(user_input, intents, context):
    user_input_lower = user_input.lower().strip()
    
    # Check context for follow-up
    if context and "follow_up" in context:
        follow_up = context["follow_up"]
        if "no" in user_input_lower and "no_response" in follow_up:
            return follow_up["no_response"], None
        elif "yes" in user_input_lower and "yes_response" in follow_up:
            return follow_up["yes_response"], None

    # Iterate through intents to find a matching pattern
    for intent in intents["intents"]:
        if any(pattern.lower() in user_input_lower for pattern in intent["patterns"]):
            response_data = random.choice(intent["responses"])
            response = response_data["response"]
            follow_up = response_data.get("follow_up", None)
            return response, follow_up
    
    return "I'm sorry, I don't understand that. Can you please rephrase?", None

# Function to display chat message
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

# Main function
def main():
    st.title("Health Organization Chatbot")
    
    # Load intents from intents.json
    intents = load_intents()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "context" not in st.session_state:
        st.session_state.context = None

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])

    # React to user input
    prompt = st.chat_input("What's up?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt)

        # Get bot response
        bot_response, follow_up = get_bot_response(prompt, intents, st.session_state.context)
        
        # Update context for follow-up
        st.session_state.context = {"follow_up": follow_up} if follow_up else None

        # Display bot response in chat message container
        display_chat_message("bot", bot_response)
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
