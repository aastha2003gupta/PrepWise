from langchain.llms import GooglePalm
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

api_key = ""
llm = GooglePalm(google_api_key=api_key, temperature=0.7)

st.title('Interview Prep Helper')

selected_option = st.selectbox("Select Option", ["Roadmap", "Interview Questions", "Notes"])

prompt = st.text_input('Enter the technology or subject for interview preparation')

roadmap_template = PromptTemplate(
    input_variables=['topic'],
    template='Give me a detailed roadmap and resource link to each step in the roadmap on {topic}'
)

interview_prep_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'],
    template='Provide an interview sheet which has 10 questions on {title}  based on Wikipedia research: {wikipedia_research}'
)

notes_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'],
    template='Provide a cheat sheet with pointers which will be helpful for interview on {title}  based on Wikipedia research: {wikipedia_research}'
)

roadmap_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history_roadmap')
interview_prep_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history_interview_prep')

roadmap_chain = LLMChain(llm=llm, prompt=roadmap_template, verbose=True, output_key='roadmap', memory=roadmap_memory)
interview_prep_chain = LLMChain(llm=llm, prompt=interview_prep_template, verbose=True, output_key='interview_prep',
                                memory=interview_prep_memory)
notes_chain = LLMChain(llm=llm, prompt=notes_template, verbose=True, output_key='notes')

wiki = WikipediaAPIWrapper()

if selected_option == "Roadmap":
    if prompt:
        wiki_research = wiki.run(prompt)
        roadmap = roadmap_chain.run(prompt)
        wiki_research = wiki.run(prompt)

        st.write("### Roadmap:")
        st.write(roadmap)

        with st.expander('Theory'):
            st.info(wiki_research)

elif selected_option == "Interview Questions":
    if prompt:
        wiki_research = wiki.run(prompt)
        interview_prep = interview_prep_chain.run(title=prompt, wikipedia_research=wiki_research)

        st.write("### Interview Preparation:")
        st.write(interview_prep)

        with st.expander('Theory'):
            st.info(wiki_research)

elif selected_option == "Notes":
    if prompt:
        wiki_research = wiki.run(prompt)
        notes = notes_chain.run(title=prompt, wikipedia_research=wiki_research)
        wiki_research = wiki.run(prompt)

        st.write("### Notes:")
        st.write(notes)

from base64 import b64encode

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}" target="_blank">{file_label}</a>'
    return href

# Add a button to download as PDF
if st.button("Download as PDF"):
    pdf_filename = "interview_prep.pdf"

    # Generate PDF content
    pdf_content = ""
    if selected_option == "Roadmap":
        pdf_content = f"Roadmap:\n\n{roadmap}\n\nTheory:\n{wiki_research}"
    elif selected_option == "Interview Questions":
        pdf_content = f"Interview Preparation:\n\n{interview_prep}\n\nTheory:\n{wiki_research}"
    elif selected_option == "Notes":
        pdf_content = f"Notes:\n\n{notes}\n\nTheory:\n{wiki_research}"

    pdf = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    style_normal = styles["BodyText"]

    # Split the content into paragraphs and add them to the PDF
    paragraphs = [Paragraph(line, style_normal) for line in pdf_content.split('\n')]
    pdf.build(paragraphs)

    # Provide download link
    st.markdown(get_binary_file_downloader_html(pdf_filename, 'Download PDF'), unsafe_allow_html=True)
