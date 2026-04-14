
# # type of the message in langchain
# # Systemmessage, Humanmessage, AlMessage
# faiss-cpu tiktoken python-dotevn
import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import JSONLoader

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_chroma import Chroma

# load_dotenv()


# model = OllamaLLM(
#     model="llama3.2:3b",
#     timeout=120  # increase timeout
# )


# prompt = PromptTemplate(
#     template = 'how many  customer are there in the data ?'
# )

# parser = StrOutputParser()

# loader = JSONLoader(
#     file_path="documents.json",
#     jq_schema=".[]",
#     content_key="page_content",
#     metadata_func=lambda x, _: x["metadata"]  
# )

# docs = loader.load()
# # print(type(docs))
# # print(len(docs))
# # print(docs[0])
# print(docs[0])
# # print(docs[0]).content

# chain = prompt | model | parser
# print (chain.invoke(prompt))

# --------------------------------------------------------------------------------------------------------

# pip install -q youtube-transcript-api langchain-community langchain-openai \
# faiss-cpu tiktoken python-dotevn
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_ollama import OllamaLLM
# from langchain_ollama import OllamaEmbeddings, ChatOllama
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import PromptTemplate
# from langchain_community.document_loaders import JSONLoader


# ---------------------------------------------------#Step 1a - indexing(Document Ingestion)
# loader = JSONLoader(
#     file_path="documents.json",
#     jq_schema=".[]",
#     content_key="page_content",
#     metadata_func=lambda x, _: x["metadata"]
# )

# docs = loader.load()

# if not docs:
#     st.error("No data available!")
#     st.stop()

# ---------------------------------------------------------# step 1b - Indexing (Text Splitting)

# splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# chunks = splitter.split_documents(docs)

# splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# chunks = splitter.split_documents(docs)

# ----------------------------------------------------# step 1c & 1d - indexing (Embedding Generation and storing in Vector Store)
# embeddings = OllamaEmbeddings(model="nomic-embed-text")  # Use a local embedding model
# vector_store = FAISS.from_documents(chunks, embeddings)

# -------------------------------------------------------# Step 2 Retrieval
# retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})

# ---------------------------------------------------------------# step 3 Augmentation
# model = OllamaLLM(model="llama3.2:3b", temperature=0.2)

# prompt = PromptTemplate(
#     template="""
# You are a helpful assistant.
# Answer ONLY from the provided transcript context.
# If the context is insufficient, just say you don't know.

# {context}
# Question: {question}
# """,
#     input_variables=['context', 'question']
# )

# --------------------------------------------# Step 4 - Generation and Chain

# from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
# from langchain_core.output_parsers import StrOutputParser

# def format_docs(retrieved_docs):
#     context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
#     return context_text

# parallel_chain = RunnableParallel({
#     'context': retriever | RunnableLambda(format_docs),
#     'question': RunnablePassthrough()
# })

# parser = StrOutputParser()

# main_chain = parallel_chain | prompt | model | parser

# ------------------------------- Streamlit UI -------------------------------
# st.set_page_config(page_title="RAG Chatbot")

# st.title("📊 RAG Chatbot with JSON Data")

# user_question = st.text_input("Ask your question:")

# if user_question:
#     st.write("### 🤖 Answer:")
#     answer = main_chain.invoke(user_question)
#     st.write(answer)




















import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import JSONLoader
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# ------------------ Step 1: Load Data ------------------
loader = JSONLoader(
    file_path="documents.json",
    jq_schema=".[]",
    content_key="page_content"
)

docs = loader.load()

if not docs:
    st.error("No data available!")
    st.stop()

# ------------------ Step 2: Split ------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

# ------------------ Step 3: Embedding + Vector Store ------------------
@st.cache_resource
def create_vector_store():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return FAISS.from_documents(chunks, embeddings)

vector_store = create_vector_store()

# ------------------ Step 4: Retriever ------------------
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2}
)

# ------------------ Step 5: Model ------------------
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0.2
)

# ------------------ Step 6: Prompt ------------------
prompt = PromptTemplate(
    template="""
You are a helpful assistant.
Answer ONLY from the provided context.
If not found, say "I don't know".

Context:
{context}

Question: {question}
""",
    input_variables=['context', 'question']
)

# ------------------ Step 7: Chain ------------------
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
})

main_chain = parallel_chain | prompt | model | StrOutputParser()

# ------------------ UI ------------------
st.set_page_config(page_title="RAG Chatbot")
st.title("📊 RAG Chatbot with JSON")

question = st.text_input("Ask something:")

if question:
    response = main_chain.invoke(question)
    st.write(response)


