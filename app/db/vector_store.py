import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.util import get_file_path
from langchain_community.embeddings import GPT4AllEmbeddings

FAISS_INDEX_FILE = "data/db_faiss"

class VectorDatabase:
    def __init__(self, index_file: str = FAISS_INDEX_FILE):
        self.index_file = index_file
        #https://openai.com/api/pricing/
        # self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
        gpt4all_kwargs = {'allow_download': 'True'}
        embedding_model = GPT4AllEmbeddings(
            model_name=model_name,
            gpt4all_kwargs=gpt4all_kwargs
        )
        self.embeddings=embedding_model
        if os.path.exists(index_file):
            self.index = FAISS.load_local(index_file, self.embeddings, allow_dangerous_deserialization= True)
        else:
            self.index = FAISS.from_texts(["None"], self.embeddings)

    def add_text(self, text: str, metadata: dict):
        """
        Add a new text to the FAISS vector store.
        """
        self.index.add_texts([text], [metadata])
        self.index.save_local(self.index_file)

    def search(self, query: str, k: int = 5):
        """
        Perform a similarity search with the query text.
        """
        return self.index.similarity_search(query, k)

vector_db = VectorDatabase()
