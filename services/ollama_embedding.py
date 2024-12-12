from langchain.embeddings.base import Embeddings
from typing import List
import ollama

class OllamaEmbeddings(Embeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
   
        embeddings = []

        for text in texts:
            response = ollama.embeddings(
                model="paraphrase-multilingual", 
                prompt=text
            )
            
            if 'embedding' in response:
                embeddings.append(response['embedding']) 
            else:
                raise ValueError(f"Failed to get embedding for text: {text}")
        
        return embeddings

    def embed_query(self, query: str) -> List[float]:

        response = ollama.embeddings(
            model="paraphrase-multilingual", 
            prompt=query
        )

        if 'embedding' in response:
            return response['embedding']
        else:
            raise ValueError(f"Failed to get embedding for query: {query}")


