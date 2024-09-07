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


# loading the environment variables
load_dotenv()



working_dir = os.path.dirname(os.path.abspath(__file__))




# loading the document/pdf
def load_document(file_path):
    loader = UnstructuredPDFLoader(file_path)
    documents = loader.load() # unstructured loader le load garekko lai document form maa load garxa
    return documents






