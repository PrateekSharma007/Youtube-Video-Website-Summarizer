
import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader


## sstreamlit APP
st.set_page_config(page_title="Summarize Text From YT or Website")
st.title("Summarize Text From YT or Website")
st.subheader('Summarize URL')


string = "0gsk_ThKTskzlyNjl2rJNgLbgWGdyb3FYjuRQERCV1I7n5bLryFYKRW3P"

## Get the Groq API Key and url(YT or website)to be summarized
with st.sidebar:
    # groq_api_key=st.text_input("Groq API Key",value="",type="password")
    groq_api_key = string[1:]

generic_url=st.text_input("URL",label_visibility="collapsed")

## Gemma Model USsing Groq API
llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

prompt_template="""
Summarize the key points of the following YouTube video in 300 words. Ensure the summary captures the main themes, key moments, and any notable elements, whether it's a song, tutorial, or any other type of content:
Content:{text}

"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize the Content from YT or Website"):
    ## Validate all the inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid Url. It can may be a YT video utl or website url")

    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website or yt video data
                if "youtube.com" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs=loader.load()

                ## Chain For Summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception:{e}")
                    