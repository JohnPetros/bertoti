from os import getenv

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


def load_documents(diretorio="./artefacts", padrao="**/*.pdf"):
    loader = DirectoryLoader(diretorio, glob=padrao, loader_cls=PyPDFLoader)
    documents = loader.load()
    print(f"{len(documents)} documents loaded.")
    return documents


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"{len(chunks)} chunks created.")
    return chunks


def create_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return embeddings


def create_vector_database(embeddings, chunks):
    vector_database = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./vector-database",
    )
    print(f"{len(chunks)} chunks indexed in ChromaDB")
    return vector_database


def create_retrieval_question_answer_chain(vector_database):
    api_key = getenv("OPENROUTER_API_KEY")
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        model="qwen/qwen3-8b:free:free",
    )
    retriever = vector_database.as_retriever()
    system_prompt = """
    Answer the question based only on the following context:
    {context}
    ---
    Answer the question based on the above context: {input}
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    question_answer_chain = create_retrieval_chain(retriever, stuff_documents_chain)
    return question_answer_chain


documents = load_documents()
chunks = split_documents(documents)
embeddings = create_embeddings()
vector_database = create_vector_database(embeddings, chunks)


def query_user_guide_pdf(query: str) -> str:
    """
    Query the user guide pdf using the vector database.
    Args:
        query: The query to search the user guide pdf.
    Returns:
        The answer to the query.
    """
    print(f"PDF query: {query}")
    question_answer_chain = create_retrieval_question_answer_chain(vector_database)
    print(f"PDF query result: {question_answer_chain.invoke({'input': query})}")
    return question_answer_chain.invoke({"input": query})
