import requests

from transformers import pipeline
from sentence_transformers import SentenceTransformer

def token_classification_service(msg : str):
    ans = pipeline("token-classification", model='vblagoje/bert-english-uncased-finetuned-pos')(msg)
    for element in ans:
        element["score"] = element["score"].item() 

    return ans

