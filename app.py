
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma 
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate
from langchain_core.messages import AIMessage,HumanMessage
import os
import streamlit as st
import nltk

nltk.download('punkt')
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

st.title("Empowering PDF Document Search with AI")
st.caption("Search content within the document")

chunks = []

## Models Initialisation ##
e_model = GoogleGenerativeAIEmbeddings(google_api_key=os.environ["GOOGLE_API_KEY"],model="models/embedding-001") # type: ignore
model = ChatGoogleGenerativeAI(google_api_key=os.environ["GOOGLE_API_KEY"],model="gemini-1.5-pro-latest") # type: ignore


############################## Document Loader & Spliiter #############################
def document_loader(uploaded_file):
     # type: ignore
    global chunks
    loader = PyPDFLoader(uploaded_file)
    pages = loader.load_and_split()    

    ##### Chunking #####
    from langchain_text_splitters import NLTKTextSplitter
    splitter = NLTKTextSplitter(chunk_size=100,chunk_overlap=0)
    chunks = splitter.split_documents(pages)
        
    vector_store(chunks)


 ######## Stroing the chunks in chroma db in text embeddings ##########
def vector_store(chunks):
    db = Chroma.from_documents(chunks, embedding=e_model,persist_directory="./rag_chromadb") # type: ignore


def retr():
    ####### retriving from db #######
    db_connection = Chroma(persist_directory="./rag_chromadb",embedding_function=e_model)
    retriver = db_connection.as_retriever(search_kwargs={"k":10}) #retriver top 5 document based on the search 
    return retriver


########################### Prompt Template ################################
chat_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpfull AI Chatbot"),
    HumanMessage("Hello"), # type: ignore
    AIMessage("Hi ! I'm your helpful Ai Assitance"), # type: ignore
    HumanMessagePromptTemplate.from_template([
        '''Answer the question based on the given context: {context}
           Question : {question}
           Answer : 
        '''
    ])
])

########################## Output Parser ###################################
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()


############################ Chains ########################################
def format_doc(docs):
    return "\n\n".join([chunk.page_content for chunk in chunks])


from langchain_core.runnables import RunnablePassthrough
rag_chain = {"context":retr() | format_doc,"question":RunnablePassthrough()} | chat_template | model| output_parser



def main():
    if uploaded_file := st.file_uploader("Upload your pdf file here"):
        with open(uploaded_file.name,"wb") as file:
            data = uploaded_file.getvalue()
            file.write(data)        
        document_loader(uploaded_file.name)
        
        if query := st.text_input("Enter your query here"):
            response = rag_chain.stream(query)
            st.write_stream(response)


if __name__ == "__main__":
    main()
