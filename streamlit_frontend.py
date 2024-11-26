import streamlit as st
from vector_store import FlowerShopVectorStore

# import chatbot
from chatbot import app
from langchain_core.messages import AIMessage, HumanMessage

st.set_page_config(layout='wide', page_title='Flower Shop Chatbot', page_icon='💐')
# vector_store = FlowerShopVectorStore()    # Knowledge base doesn't have to be initialized here because the chatbot graph already has access

if 'message_history' not in st.session_state:
    st.session_state.message_history = [AIMessage(content="Hiya, Im the flower shop chatbot. How can I help?") ]

left_col, main_col, right_col = st.columns([1, 2, 1])

# 1. Buttons for chat - Clear Button

with left_col:
    if st.button('Clear Chat'):
        st.session_state.message_history = []
        

# 2. Chat history and input
with main_col:
    user_input = st.chat_input("Type here...")

    if user_input:
        
    # No More calling the Knowledge Base directly. We shall be using the ChatModel LL chain
        st.session_state.message_history.append(HumanMessage(content=user_input))
        
        # Invoke the LLM with user_input -- All message history until when we start to use langgraph autonomously
        
        response = app.invoke(
            {
                "messages": st.session_state.message_history
            }
        )
        
        # Update chat history and response
        st.session_state.message_history = response['messages']
        
    for i in range(1, len(st.session_state.message_history) + 1):
        this_message = st.session_state.message_history[-i]
        
        # choose which role Type to display on chat based on AI or Human message
        if isinstance(this_message, AIMessage):
            message_box = st.chat_message("assistant")
            
        else: 
            message_box = st.chat_message("user")
        
        # Display message content    
        message_box.markdown(this_message.content)
# 3. State variables

with right_col:
    st.text(st.session_state.message_history[-1])