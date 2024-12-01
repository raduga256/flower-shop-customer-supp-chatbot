from langgraph.graph import StateGraph, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage

from langchain_groq import ChatGroq
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser

# Import ToolNode
from langgraph.prebuilt import ToolNode
from tools import (query_knowledge_base,
                   search_for_product_recommendations,
                   data_protection_check,
                   create_new_customer)


# import API keys
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from a.env file
_ = load_dotenv(find_dotenv())

#openai_api_key = os.environ["OPENAI_API_KEY"]

# Load opensource api models
groql_api_key = os.environ["GROQ_API_KEY"]

# Load LangChain LangSmith Tracking APIs
os.environ["LANGCHAIN_TRACING_V2"] = "true" # Signal start tracking
langchain_api_key = os.environ["LANGCHAIN_API_KEY"]

# Instantiate the  model

# # specify llama model
# llamaChatModel = ChatGroq(
#     model="llama3-70b-8192"
# )

# specify Gemma model
gemmaChatModel = ChatGroq(
    model="Gemma2-9b-It"
)

output_parser = StrOutputParser()



# we using prebuilt *MessagesState* for messages state that will be parsed by around to node and graph.
# Ratherthan using a custom Messages because ...we need only a single message state

# Add prompt that will used as we Incorporate ChatModel into the graph

prompt = """#Purpose 

You are a customer service chatbot for a flower shop company. You can help the customer achieve the goals listed below.

#Goals

1. Answer questions the user might have relating to serivces offered
2. Recommend products to the user based on their preferences
3. Retrieve or create customer profiles. If the customer already has a profile, perform a data protection check to retrieve their details. If not, create them a profile.

#Tone

Helpful and friendly. Use gen-z emojis to keep things lighthearted. You MUST always include a funny flower related pun in every response.
"""
# Create prompt Template
chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', prompt),
        ('placeholder', "{messages}")       # placeholder is used to parse into our extisting message history and any other variables
    ]
)

# Register our tools that we shall BIND to the LLM
tools = [query_knowledge_base, search_for_product_recommendations, data_protection_check, create_new_customer]
                   

# Chains using LECL --> combine chat-prompt with LLM
# llm_with_prompt = chat_template | gemmaChatModel | output_parser
llm_with_prompt = chat_template | gemmaChatModel.bind_tools(tools) #| output_parser disabled causes HumanMessae errors


# define our call_agent function
def call_agent(messsage_state: MessagesState):
    # incorporate the chat LLM chain into our call_agent
    response = llm_with_prompt.invoke(messsage_state)       # Response is a single key: message state returned
    
    # returns a dict of messages history using MessagesState class key "messages"
    return{
           "messages":[response]        #Insert twice to see history of messages manually inspection
           }

##########################
# Add tools Node to the Graph

tool_node = ToolNode(tools) # create a ToolNode


# Create a function that checks if there Tools are available to call
# Routes the traffic according what the LLM agent wants to do otherwise go to the end of the graph.
def is_there_tool_calls(state:MessagesState):
    # checking last message/state if it has a tool request.
    last_message = state['messages'][-1]
    
    if last_message.tool_calls:
        return "tool_node"
    
    else:
        return "__end__" # end of the graph
    
    

# Create graph
graph = StateGraph(MessagesState)

# Add a single node that calls the agent_node i.e custom function
graph.add_node("agent", call_agent)   # determines the agent to call custom function

# Adding a edge between the agent to the end of the graph. Because the LLM is not using tools at this stage
# otherwise create a conditional edge between the agent and tools.
# graph.add_edge("agent", "__end__") # connects the agent to the end of the graph

graph.add_node('tool_node', tool_node)
graph.add_conditional_edges(
    'agent',
    is_there_tool_calls
)
# Always add an edge from the tool_node back to our agent
# tools_agent should not end with without call  to the agent_node
graph.add_edge(
    "tool_node", 
    "agent"
)

# Stating the entry point to the grapgh
graph.set_entry_point("agent")

# compile the graph
app = graph.compile()


# Pass this function call to the Frontend streamlit
# Invoke the graph
# updated_messages = app.invoke({
#     "messages": [HumanMessage(content="Hello, Jo")] 
# })

# print(updated_messages) # run script in terminal
