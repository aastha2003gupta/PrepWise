import langchain
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
import textwrap
from PyPDF2 import PdfReader

api_key = 'AIzaSyC4GEY4Ir_SZ2fp9TS03SwF_R9rpPTFm38'
llm = GooglePalm(google_api_key=api_key, temperature=0.7)

# Function to get text from a PDF file
def get_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

st.title('Cover Letter Generator')

position = st.text_input('Position:')
company = st.text_input('Company:')

# Upload resume (PDF or TXT)
resume_upload = st.file_uploader('Upload Your Resume (PDF or TXT)', type=['pdf', 'txt'])

# Generate cover letter on button click
if st.button('Generate Cover Letter'):
    if resume_upload:
        # Extract text from the uploaded resume
        if resume_upload.type == 'application/pdf':
            resume_content = get_text_from_pdf(resume_upload)
        else:
            resume_content = resume_upload.read()

        # Template for the cover letter
        prompt_template = PromptTemplate(
            input_variables=['position', 'company', 'resume'],
            template='Use information from :{resume} and draft cover letter highlighting all the skills and education and experiences. First paragraph should contain introduction along with skills and education, second should have experience and projects and the third should be a conclusion :Dear Hiring Manager,\n\nI am writing to apply for the {position} position at {company}.Sincerely,\n[Your Name]'
        )

        # Create the LLMChain
        llm_chain = LLMChain(llm=llm, prompt=prompt_template)

        # Run the chain to generate the cover letter
        cover_letter = llm_chain.run(position=position, company=company,resume=resume_content)

        # Wrap the text for better display
        wrapped_text = textwrap.fill(cover_letter, width=80, break_long_words=False, replace_whitespace=False)

        # Display the generated cover letter
        st.subheader('Generated Cover Letter:')
        st.text(wrapped_text)
    else:
        st.warning("Please upload your resume before generating the cover letter.")
