# Creating our Vector Store

import json
from chromadb import PersistentClient, EmbeddingFunction, Embeddings
# using llama-index to import huggingface models to use them locally on our computers
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List



# huggingface embeddings models
# https://huggingface.co/spaces/mteb/leaderboard

MODEL_NAME = 'dunzhang/stella_en_1.5B_v5'

# Add path to our local vector database - Chroma
DB_PATH = "./.chroma_db"

# Load FAQ data into chroma_db collection
FAQ_FILE_PATH = "./FAQ.json"
INVENTORY_FILE_PATH = "./INVENTORY.json"

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
        
 

# Vector db Querrying class
class FlowerShopVectorStore:
    # helps to avoid entering the data twice if it already exists
    def __init__(self):
        # Create a chroma_db persistent database
        db = PersistentClient(path=DB_PATH) # Database path
        
        # Chroma collections for topics, products and QA 

        # create a custom embedding function into chroma_db
        custom_embedding_function = CustomEmbeddingClass(MODEL_NAME)

        #create collections FAQ embedings
        self.faq_collection = db.get_or_create_collection(name='FAQ', embedding_function=custom_embedding_function)
        #create collections for inventory embeddedding
        self.inventory_collection = db.get_or_create_collection(name='Inventory', embedding_function=custom_embedding_function)
        
        # load collections IF only they have not yet been loaded
        # Avoid reloading existing data already
        if self.faq_collection.count() == 0:
            self._load_faq_collections(FAQ_FILE_PATH)   # path passed directly
            
        if self.inventory_collection.count() == 0:
            self._load_inventory_collections(INVENTORY_FILE_PATH)   # path passed directly
                
            
    # loading chroma_db FAQ collections
    def _load_faq_collections(self, faq_file_path:str):
        # Load FAQ data into chroma_db collection
        with open(faq_file_path, 'r') as f:
            faqs = json.load(f)
            
        # add to the collection
        self.faq_collection.add(
            documents=[faq['question'] for faq in faqs] + [faq['answer'] for faq in faqs],
            ids=[str(i) for i in range(0, 2*len(faqs))],
            metadatas=faqs + faqs
        )
        
     # loading chroma_db Inventory collections
    def _load_inventory_collections(self, inventory_file_path:str):
        # Load FAQ data into chroma_db collection
        with open(inventory_file_path, 'r') as f:
            inventories = json.load(f)
            
        # add to the collection
        self.inventory_collection.add(
            documents=[inventory['description'] for inventory in inventories],
            ids=[str(i) for i in range(0, 2*len(inventories))],
            metadatas=inventories + inventories
        )

    # querrying FAQ collection
    def query_faqs(self, query:str):
        return self.faq_collection.query(query_texts=[query], n_results=5)
    
    # querrying inventory collection
    def query_inventories(self, query:str):
        return self.inventory_collection.query(query_texts=[query], n_results=5)