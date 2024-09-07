import os  # working directory access garna lai 

from dotenv import load_dotenv  ## enviroment variables access garna lai 

import streamlit as st    # for user interface

from langchain_community.document_loaders import UnstructuredPDFLoader   ## pdf file read garna lai 

from langchain_text_splitters.character import CharacterTextSplitter     

from langchain_community.vectorstores import FAISS   ## facebook AI similarity search
from langchain_community.embeddings import HuggingFaceEmbeddings    # text chunks into vector embeddings (simply text chunks lai  numeric representation maa lani )

from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory  ## previous qn-ans (chat) memorize garna lai 

from langchain.chains import ConversationalRetrievalChain

from langchain.document_loaders import PyPDFLoader



# loading the environment variables
load_dotenv()



working_dir = os.path.dirname(os.path.abspath(__file__))




# loading the document/pdf
def load_document(file_path):
    loader =PyPDFLoader(file_path)
    documents = loader.load() # unstructuredPDFloader le load gareko lai document form maa load garxa
    return documents




def setup_vectorstore(documents):
    embeddings = HuggingFaceEmbeddings()
    text_splitter = CharacterTextSplitter(
        separator="/n",
        chunk_size=1000,
        chunk_overlap=200
    )


    doc_chunks = text_splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(doc_chunks, embeddings)

    # FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vector


    return vectorstore





def create_chain(vectorstore):
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0
    )
    retriever = vectorstore.as_retriever()

    ## previous chat history memory maa save garna lai
    memory = ConversationBufferMemory(
        llm=llm,
        output_key="answer",
        memory_key="chat_history",
        return_messages=True
    )


    ## A Conversational Retrieval Chain is a system that helps AI maintain context in conversations by remembering past interactions and retrieving relevant information to provide accurate and coherent responses.


    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        chain_type="map_reduce",
        memory=memory,
        verbose=True
    )
    return chain


## Setting up the user interface

st.set_page_config(
    page_title="Chat with Doc",
    page_icon="📄",
    layout="centered"
)

st.title("🦙 Chat with your document....😎")


# initialize the chat history in streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


uploaded_file = st.file_uploader(label="Upload your pdf file", type=["pdf"])

if uploaded_file:
    file_path = f"{working_dir}/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = setup_vectorstore(load_document(file_path))

    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = create_chain(st.session_state.vectorstore)

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Ask Llama...")




if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)


    with st.chat_message("assistant"):
        response = st.session_state.conversation_chain({"question": user_input})
        assistant_response = response["answer"]
        st.markdown(assistant_response)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})





