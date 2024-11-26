"""
        # Creating Tools for the Lanngraph ###
        
        the LLM will be creating their own queries but while generating response,
        
        The LLM will have to base on the tools sometimes to answer the queries.
        
        we will use these tools to fetch data from our knowledge base.
        
    """

# Importing required libraries
from langchain_core.tools import tool
from typing import List, Dict
from vector_store import FlowerShopVectorStore 


# Instantiate VectorStore
vector_store = FlowerShopVectorStore()     

# LLM will have a choice of when to use which tool.
@tool
def query_knowledge_base(query: str) -> List[Dict[str, str]]:
    """
    Looks up information in a knowledge base to help with answering customer questions and getting information on business processes.

    Args:
        query (str): Question to ask the knowledge base

    Return:
        List[Dict[str, str]]: Potentially relevant question and answer pairs from the knowledge base
    """
    
    # Return a list of dictionaries containing -Question, -Answer messages
    return vector_store.query_faqs(query=query)

@tool
def search_for_product_recommendations(description: str):
    """
    Looks up information in a knowledge base to help with product recommendation for customers. For example:

    "Boquets suitable for birthdays, maybe with red flowers"
    "A large boquet for a wedding"
    "A cheap boquet with wildflowers"

    Args:
        query (str): Description of product features

    Return:
        List[Dict[str, str]]: Potentially relevant products
    """
    
    # Return a list of dictionaries containing -Product Name, -Product Description
    return vector_store.query_inventories(query=description)
