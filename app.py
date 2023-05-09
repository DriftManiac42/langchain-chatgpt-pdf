from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


def main():
    load_dotenv()
    st.set_page_config(page_title="Ask you PDF")
    st.header("Ask your PDF...")

    # upload pdf file
    pdf = st.file_uploader("Upload your PDF", type="PDF")

    # extract text from pdf file
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # show user input
        user_question = st.text_input("Ask question about your PDF:")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            st.write(docs)
        # stop here


if __name__ == '__main__':
    main()
