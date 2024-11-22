# 1. Buttons for chat ---Clear Button

# 2. Buttons for chat history and input

# 3. State  Variables

import streamlit as st

# 4. Streamlit Web App page configuration for layout and titles
st.set_page_config(layout="wide", page_title="Flower Shop Chatbot", page_icon="🌺")

# Add session configuration for storing message history
if "message_history" not in st.session_state:
    # conditions LLM or user message for default expection
    #st.session_state.message_history = ["Hiya, Im the flower shop chatbot. How can I help you?"]

    # use dictionary to store and retrieve messages and roles
    st.session_state.message_history = [{"content": "Hiya, Im the flower shop chatbot. How can I help you?", "type": "assistant"}]
# Columns size customizations
left_col, main_col, right_col = st.columns([1, 2, 1])

# 1. Conditional Button for chat - Clear Button
with left_col:
    
    # Creates a button with a condition
    if st.button("Clear Chat"):
        st.session_state.message_history = []   # Clear current agent state or messsage

# 2. Chat message history and Input in the main col window
with main_col:
    # Get the input from user
    user_input = st.chat_input("Type here ...")
    
    # Display the inputted user input
    if user_input:
        st.text(user_input)
        # Add it to our message history
        st.session_state.message_history.append({"content": user_input, "type": "user"})

        # Loop of the message history and display it with streamlit
        # use indexing to be able to display last messages first on the screen - backwards access
        for i in range(1, len(st.session_state.message_history)+1 ):
            
            # create streamlit *chat_message* component with role metadata
            this_message = st.session_state.message_history[-i] # store last message into a variable
            
            #create streamlit *chat_message* component
            message_box = st.chat_message(this_message["type"])
            
            # print message
            message_box.markdown(this_message["content"])
            
            
    
# 3. State  Variables
with right_col:
    # Create our state in the righthand columns - on pressing clear button, message will be deleted
    st.text(st.session_state.message_history)