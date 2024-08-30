import validators
import streamlit as st 
from langchain.prompts import PromptTemplate 
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader 


##streamlit app 

st.set_page_config(page_title="Youtube/Website Summarize") 
st.title("Youtube/Website Summarize")
st.subheader("Summarize URL") 


##groq api key 

with st.sidebar: 
    groq_api_key= st.text_input("Groq API KEY" , value="password") 


url = st.text_input("URL",label_visibility="collapsed")



if st.button("Summarize the content from the URL") : 
    if not groq_api_key.strip() or not url.strip() : 
        st.error("Please provide the information")
    elif not validators.url(url) : 
        st.error("Please provide a valid URL.")

    else: 
        try : 
            with st.spinner("waiting...") : 
                 
    