import streamlit as st
from vector_store import FlowerShopVectorStore
from chatbot import app
from langchain_core.messages import AIMessage, HumanMessage
from tools import customers_database, data_protection_check

st.set_page_config(layout='wide', page_title='Flower Shop Chatbot', page_icon='💐')

if 'message_history' not in st.session_state:
    st.session_state.message_history = [AIMessage(content="Hiya, I'm the flower shop chatbot. How can I help?")]

left_col, main_col, right_col = st.columns([1, 2, 1])

# 1. Buttons for chat - Clear Button
with left_col:
    if st.button('Clear Chat'):
        st.session_state.message_history = []

# 2. Chat history and input
with main_col:
    user_input = st.chat_input("Type here...")

    if user_input:
        st.session_state.message_history.append(HumanMessage(content=user_input))

        try:
            response = app.invoke({"messages": st.session_state.message_history})
            st.session_state.message_history = response['messages']
        
        except ValueError as ve:
            if str(ve) == "No response generated":
                error_message = AIMessage(content="I'm sorry, I didn't quite understand that. Could you please rephrase your question or provide more details?")
                st.session_state.message_history.append(error_message)
            else:
                raise ve
        
        except Exception as e:
            if isinstance(e, BadRequestError):  # Custom error handling for BadRequestError
                error_message = AIMessage(content="An error occurred while processing your request. Please try again or adjust your query.")
                st.session_state.message_history.append(error_message)
                log_error(e)
            else:
                raise e

    for i in range(1, len(st.session_state.message_history) + 1):
        this_message = st.session_state.message_history[-i]

        if isinstance(this_message, AIMessage):
            message_box = st.chat_message("assistant")
        else:
            message_box = st.chat_message("user")

        message_box.markdown(this_message.content)

# 3. State variables
# with right_col:
#     st.text(st.session_state.message_history[-1])

with right_col:
    st.title('customers database')
    st.write(customers_database)
    st.title('data protection checks')
    st.write(data_protection_check)

def log_error(error):
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{error}\n")
