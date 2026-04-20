
import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import JSONLoader
from langchain_core.documents imporimport streamlit as st
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


