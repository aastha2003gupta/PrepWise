from langchain.llms import GooglePalm
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import DuckDuckGoSearchRun
from duckduckgo_search import DDGS
import json
import scrapy
import requests
from bs4 import BeautifulSoup
api_key = ""
google_llm = GooglePalm(google_api_key=api_key)

st.title('Interview Experience')
st.markdown(
        """
Gain invaluable insights into your dream job. 
Navigate the intricacies of the interview process for specific roles in top companies, empowering you with firsthand accounts to enhance your preparation and boost your confidence.
        """
    )

Role_prompt= st.text_input('Role')
Company_prompt= st.text_input('Company')

if Role_prompt and Company_prompt:
        def remove_duplicate_empty_lines(text):
            lines = text.splitlines()
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            cleaned_text = '\n'.join(cleaned_lines)
            return cleaned_text
        interview_template = PromptTemplate(
            input_variables=['prompt_role','prompt_company', 'duckduckgo_research'],
            template ="""
                Here is some text extracted from the webpage by bs4:
                ---------
                {duckduckgo_research}
                ---------

                Web pages can have a lot of useless junk in them. 
                For example, there might be a lot of ads, or a 
                lot of navigation links, or a lot of text that 
                is not relevant to the topic of the page. We want 
                to extract only the useful information from the text.

                You can use the url and title to help you understand 
                the context of the text.
                Please extract only the useful information from the text. 
                Try not to rewrite the text, but instead extract 
                only the useful information from the text.

                I want to extract detailed Interview Experience for the role of :{prompt_role} in company:{prompt_company} from the above extracted text , dont make anything up
            """
        )
        interview_chain = LLMChain(llm=google_llm, prompt=interview_template, verbose=True, output_key='experience')


        extracted_text = ''
        with DDGS() as ddgs:
            results = list(ddgs.text(f'Geeks for Geeks Interview Experience of {Role_prompt} in {Company_prompt}', region='wt-wt', safesearch='off', timelimit='y', max_results=1))
        urls = [result['href'] for result in results]

        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                title = soup.title.string
                text = soup.get_text()
                cleaned_text = remove_duplicate_empty_lines(text)

                extracted_text += cleaned_text + '\n\n'  

                
        try:
            max_bytes = 50000
            if len(extracted_text.encode('utf-8')) > max_bytes:
                reduction_factor = max_bytes / len(extracted_text.encode('utf-8'))
                new_text_length = int(len(extracted_text) * reduction_factor)
        
                extracted_text = extracted_text[:new_text_length]
            experience= interview_chain.run(prompt_role=Role_prompt,prompt_company=Company_prompt, duckduckgo_research=extracted_text)
            if experience:
                st.write(experience)
            else:
                
                st.write("No information found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")


