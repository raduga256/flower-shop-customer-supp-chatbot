# flower-shop-customer-supp-chatbot

This project focuses on building a customer support agent/chatbot in python for an online flower shop using:

Probably be used for ordering flowers for an anniversay or valentine. Customers can also ask about the business processes such as order deliveries

1. Streamlit (frontend)
2. LangGraph (agent logic)
3. Chromadb (local vector database)
4. HuggingFace (RAG embedding model)
5. LlamaIndex  (local hosting)


## Features to Build:
I will build features into the chatbot such as:
- Managing customer profiles
- Getting customer order updates
- Placing customer orders
- Answering customer FAQ
- Getting product reccommendations

## Project Breakdown:
- *Part 1:* Project folders setup and Streamlit
- *Part 2:*	FAQ and product Recommendation
### Major Goal: Create a local RAG database
Create and Ultilize a Local RAG 
 
 we will setup a local RAG database with ChromaDB, HuggingFace and LlamaIndex in order to be able to retrieve relevant products and FAQ questions. We will also connect it to the frontend we built in the previous episode to test it interactively.

 In this part of the tutorial we created a vector database with ChromaDB, and connected it to our streamlit frontend. With this setup we were able to ask FAQ style questions and also ask for product recommendations for our Flower Shop. Within the chroma database we created two knowledge base collections:

FAQ Question and Answer pairs
Product descriptions
We also updated the front end to choose between which knowledge base e.g Inventory to query:

 #### Objectives
0. - What to will build;
1. - Setting up FAQs & Product reccommendations
3. - New packages
4. - Finding RAG embedding model 
5. - Local Vector Database (Chroma)  
6. - LlamaIndex Embeddings
7. - Ingest FAQs into Vector DB
8. - Querying Vector DB
9. - Update Streamlit Frontend
10. - Tidy up python 
11. - Adding Product Inventory
12. - Adding Radio Button to guide user on which knowledge base to query i.e FAQ or Inventory descriptions


- #### *Part 3:* Langgraph
Libraries Needed:
langchain-openai
python-dotenv
langchain-groq
langgraph

will setup LangGraph to act as an an Agentic Chatbot. We will connect our Agent with the RAG database we setup in the last episode with two tools that the Agent can use to retrieve information on demand. We will use few shot prompting in our tool definition to teach our language model how to use them effectively

##### Processes
- What we will build
- Package Setup
- Setup LangGraph without prompt
- Test with single node
- Create Prompt
- ChatTemplate
- Create LLM Intialisation
- Use LLM in node
- Cmd line test of script
- Connect to frontend
- Test Frontend
- Create tool for Querying Knowledge base ---> tools.py 
- Product Reccommendation tool ---> tools.py 
- Add tools to LangGraph Agent
- LangGraph Conditional Edge
- Updating frontend & testing



- #### *Part 4:* Customer Management


- #### *Part 5:* Order Management