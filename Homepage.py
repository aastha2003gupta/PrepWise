import streamlit as st

st.set_page_config(
    page_title="PrepWise"
)

st.sidebar.success("Select a page above")


st.title("Welcome to Prepwise")

    # Introduction
st.markdown(
        """
        PrepWise is an interview helper app which is designed to support you in getting ready for job interviews. Whether you need a comprehensive roadmap, interview questions or experience, or helpful cheat sheets, we have you covered. Additionally, you can create a personalized cover letter. Begin by selecting a page from the sidebar to initiate the process.

        """
    )

    # Image
st.image("preppic.svg", caption="Interview Preparation", use_column_width=True)

    # Additional Information
st.markdown(
    """
    **Tips for Successful Interview Preparation:**

    **Thorough Research:**
    - Understand the company's history, values, and the role you're applying for.
    - Stay updated on industry trends to demonstrate industry knowledge.

    **Practice Responses:**
    - Rehearse common interview questions and articulate your strengths and experiences.
    - Prepare examples for behavioral questions that showcase your skills.

    **Professional Presentation:**
    - Dress professionally in alignment with the company culture.
    - Maintain positive body language and a polished appearance.

    **Effective Communication:**
    - Know your resume thoroughly and discuss key accomplishments.
    - Develop insightful questions for the interviewer to express genuine interest.

    **Post-Interview Etiquette:**
    - Send a prompt thank-you email, expressing gratitude and reiterating interest.
    - Stay positive, confident, and enthusiastic throughout the interview process.

    Good luck with your interview preparation!
    """
)
 