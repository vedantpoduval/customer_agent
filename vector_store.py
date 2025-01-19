from chromadb import PersistentClient,EmbeddingFunction,Embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List
import json
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
DB_PATH = './.chroma_db'


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

db = PersistentClient()
custom_embedding_function = CustomEmbeddingClass(MODEL_NAME)
collection = db.get_or_create_collection(name="FAQ",embedding_function=custom_embedding_function)

faq_file_path = "./FAQ.json"

with open(faq_file_path,'r') as f:
    faqs = json.load(f)

collection.add(
    documents=[faq['question'] for faq in faqs] + [faq['answer'] for faq in faqs],
    ids = [str(i) for i in range(0,2*len(faqs))],
    metadatas=faqs + faqs
)

def query_faqs(query):
    return collection.query(query_texts=[query],n_results=5)