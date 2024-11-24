# Creating our Vector Store

import json
from typing import Any
from chromadb import PersistentClient, EmbeddingFunction, Embeddings
# using llama-index to import huggingface models to use them locally on our computers
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List




# huggingface embeddings models
# https://huggingface.co/spaces/mteb/leaderboard

MODEL_NAME = 'dunzhang/stella_en_1.5B_v5'

# Add path to our local vector database - Chroma
DB_PATH = "./.chroma_db"

# Create python code to represent all objects stored in the FAQ and Inventory json files

# Class to represent products in inventory
class Product:
    def __init__(self, name: str, id: str, description: str, type: str, price: float, quantity: int):
        self.name = name
        self.id = id
        self.description = description
        self.type = type
        self.price = price
        self.quantity = quantity

# Class to represent FAQ items
class QuestionAnswerPairs:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer
        
# cReating a custom embedding class to be used by chromaDB to embed queries and retrieval
class CustomEmbeddingClass(EmbeddingFunction):      # inherits from EmbeddingFunction
    # used to load the embedding model downloaded by Lamma-Index to be able to use them locally
    def __init__(self, model_name=MODEL_NAME):
        
        # Instantiates a new Embedding model
        self.embedding_model = HuggingFaceEmbedding(model_name=MODEL_NAME)
    
    # Takes input text and returns chroma embeddings =>> import chroma Embeddings
    def __call__(self, input_texts: List[str]) -> Embeddings:
        
        # Embedding the input text using the model
        return [self.embedding_model.get_text_embedding(text) for text in input_texts]


############################################
""" Code below will have to be put into a Class with function"""

############################################

        
# Create a chroma_db persistent database
db = PersistentClient(path=DB_PATH) # Database path

# Chroma collections for topics, products and QA 

# create a custom embedding function into chroma_db
custom_embedding_function = CustomEmbeddingClass(MODEL_NAME)

collection = db.get_or_create_collection(name='FAQ', embedding_function=custom_embedding_function)

# Load FAQ data into chroma_db collection
faq_file_path = "./FAQ.json"

with open(faq_file_path, 'r') as f:
    faqs = json.load(f)
    
# add to the collection
collection.add(
    #embed both the question and the answer as seperate documents using 2 lists
    documents=[faq['question'] for faq in faqs] + [faq['answer'] for faq in faqs],
    
    # id of each document using a dummy id
    ids=[str(i) for i in range(0, 2*len(faqs))],
    
    # create and pass metadata associated with the embeddings. Takes the full QA files
    metadatas=faqs + faqs 
    
)

# Query the db and limit top returned closest results as a function

def query_faqs(query):
    collection.query(query_texts=[query], n_results=5)
    # import this into the front end script. Each time a user enters a query its embbedded first
    
    



