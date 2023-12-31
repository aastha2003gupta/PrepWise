import streamlit as st
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from langchain.prompts import PromptTemplate
from langchain.llms import GooglePalm
from langchain.chains import LLMChain

api_key = "AIzaSyC4GEY4Ir_SZ2fp9TS03SwF_R9rpPTFm38"
llm = GooglePalm(google_api_key=api_key, temperature=0.7)

def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_summary(text, sentences_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=sentences_count)
    text = ' '.join(str(sentence) for sentence in summary)
    summary_template = PromptTemplate(
        input_variables=['text','lines'],
        template="""
        Given text {text} is a summary of a PDF. 
        I want to make detailed summary in a presentable format ,do not exceed the given number of lines {lines}.Do not make anything up
    """
    )
    
    llm_chain = LLMChain(llm=llm, prompt=summary_template, verbose=True)
    text_summary = llm_chain.run(text=text,lines=sentences_count)
    return text_summary

def generate_detailed_notes(text):
    # Modify this function to generate detailed notes using your desired method
    notes_template = PromptTemplate(
        input_variables=['text'],
        template="""
        Given text {text} is a summary of a PDF. 
        I want to make detailed and presentable notes out of it.
    """
    )
    
    llm_chain = LLMChain(llm=llm, prompt=notes_template, verbose=True)
    notes = llm_chain.run(text=text)
    return notes

st.title("PDF Summarizer and Notes Maker")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        raw_text = get_pdf_text(uploaded_file)

        generate_option = st.radio("Select an option:", ["Summary", "Detailed Notes"])

        if generate_option == "Summary":
            st.subheader("Summary:")
            sentences_count = st.slider("Select the number of sentences for the summary:", 1, 20, 5)
            summarized_text = generate_summary(raw_text, sentences_count)
            st.write(summarized_text)

        elif generate_option == "Detailed Notes":
            detailed_notes = generate_detailed_notes(raw_text)
            st.subheader("Detailed Notes:")
            st.write(detailed_notes)

        if st.button("Save"):
            filename = f"{generate_option.lower().replace(' ', '_')}_output.txt"
            with open(filename, "w") as output_file:
                if generate_option == "Summary":
                    output_file.write("Summary:\n" + summarized_text + "\n")
                elif generate_option == "Detailed Notes":
                    output_file.write("Detailed Notes:\n" + detailed_notes + "\n")

            st.success(f"{generate_option} saved to {filename}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

