from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from pathlib import Path

class LegalRetrieverRAG:
    def __init__(self, docs_path="legal_docs"):
        self.docs_path = docs_path
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=float(os.getenv("RAG_LLM_TEMPERATURE", "0.1")),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            convert_system_message_to_human=True
        )
        self.embedding = GoogleGenerativeAIEmbeddings()
        self._initialize_vectorstore()
        self._initialize_qa_chain()

    def _initialize_vectorstore(self):
        documents = []
        for file in Path(self.docs_path).glob("*.txt"):
            loader = TextLoader(str(file))
            documents.extend(loader.load())
        self.vectorstore = FAISS.from_documents(documents, self.embedding)
        self.retriever = self.vectorstore.as_retriever()

    def _initialize_qa_chain(self):
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True
        )

    def answer_query(self, query: str):
        result = self.qa_chain({"query": query})
        answer = result["result"]
        sources = [doc.metadata.get("source", "") for doc in result["source_documents"]]
        return {"answer": answer, "sources": sources} 