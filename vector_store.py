from chromadb import PersistentClient,EmbeddingFunction,Embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List
import json
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
DB_PATH = './.chroma_db'
FAQ_PATH = "./FAQ.json"
INVENTORY_PATH = "./inventory.json"

class Product:
    def __init__(self,id:str,name:str,quantity:int,price:float,type:str,description:str):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.type = type
        self.description = description
class QuestionAnsPairs:
    def __init__(self,question:str,answer:str):
        self.question = question
        self.answer = answer
class CustomEmbeddingClass(EmbeddingFunction):
    def __init__(self,model_name):
        self.embedding_model = HuggingFaceEmbedding(model_name)
        
    def __call__(self, input_texts: List[str]) -> Embeddings:
        return [self.embedding_model.get_text_embedding(text) for text in input_texts]


class FlowerShopVector:
    def __init__(self):
        db = PersistentClient(path=DB_PATH)
        custom_embedding_function = CustomEmbeddingClass(MODEL_NAME)
        self.faq_collection = db.get_or_create_collection(name="FAQ",embedding_function=custom_embedding_function)
        self.inventory_collection = db.get_or_create_collection(name="INVENTORY",embedding_function=custom_embedding_function)

        if self.faq_collection.count() == 0:
            self.load_faq_data_collection(FAQ_PATH)
        if self.inventory_collection.count() == 0:
            self.load_inv_data_collection(INVENTORY_PATH)
    def load_faq_data_collection(self,faq_file_path:str):          
        with open(faq_file_path,'r') as f:
            faqs = json.load(f)

        self.faq_collection.add(
            documents=[faq['question'] for faq in faqs] + [faq['answer'] for faq in faqs],
            ids = [str(i) for i in range(0,2*len(faqs))],
            metadatas=faqs + faqs
        )
    def load_inv_data_collection(self,inv_file_path:str):          
        with open(inv_file_path,'r') as f:
            inventories = json.load(f)

        self.inventory_collection.add(
            documents=[inventory['description'] for inventory in inventories],
            ids = [str(i) for i in range(0,len(inventories))],
            metadatas=inventories
        )
    def query_faqs(self,query):
        return self.faq_collection.query(query_texts=[query],n_results=5)
    def query_inventories(self,query):
        return self.inventory_collection.query(query_texts=[query],n_results=5)