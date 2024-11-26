from langgraph.graph import StateGraph, MessagesState
# we using prebuilt *MessagesState* for messages state that will be parsed by around to node and graph.
# Ratherthan using a custom Messages because ...we need only a single message state

# define our call_agent function
def call_agent(messsage_state: MessagesState):
    print(messsage_state)   # print prexisting message state from the last node execution
    example_message = "Hello world "
    
    # returns a dict of messages history using MessagesState class key "messages"
    return{
           "messages":[example_message, example_message]        #Insert twice to see history of messages manually inspection
           }


# Create graph
graph = StateGraph(MessagesState)

# Add a single node that calls the agent_node i.e custom function
graph.add_node("agent", call_agent)   # determines the agent to call custom function

# Adding a edge between the agent to the end of the graph.
graph.add_edge("agent", "__end__") # connects the agent to the end of the graph

# Stating the entry point to the grapgh
graph.set_entry_point("agent")

# compile the graph
app = graph.compile()

# Invoke the graph
updated_messages = app.invoke({
    "messages":['Hello, Paulson']  
})

print(updated_messages) # run script in terminal
