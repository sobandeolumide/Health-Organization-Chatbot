import streamlit as st
from chatbot import handle_input

def main():
    st.title("Health Organization Chatbot")
    
    # Input field for user to enter message
    user_input = st.text_input("Enter your message:", "")

    if st.button("Send"):
        # Call the handle_input function with the user's message
        bot_response = handle_input(user_input)
        # Display the bot's response
        st.text_area("Bot's Response:", bot_response, height=200)

# Call the main function
if __name__ == "__main__":
    main()
