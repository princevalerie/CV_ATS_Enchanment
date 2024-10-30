import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import fitz  


load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
model = genai.GenerativeModel('gemini-1.5-pro')

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def improve_cv_general(cv_text):
    prompt = f"""
        As an ATS (Applicant Tracking System) and CV enhancement expert, please thoroughly review the following CV and make it more optimized for ATS compatibility. Pay special attention to any issues that could affect ATS parsing, including formatting, keyword relevance, and quantifiable achievements, especially in the experience section.

        ### Instructions for Optimization

        #### 1. **Correct Formatting and Layout for ATS Compatibility**
        - Ensure the CV has a simple, ATS-friendly layout (no tables, graphics, or complex formatting).
        - Use a consistent font and spacing style throughout the CV. Recommended fonts include Arial, Calibri, or Times New Roman, with a font size between 10 and 12 points.
        - Organize sections clearly with appropriate headings like "Experience," "Education," and "Skills" for easy ATS reading. Use bold or larger font for these headings to enhance readability.

        #### 2. **Experience Section - Quantitative Enhancements**
        - In the experience section, ensure that each job description includes specific, measurable achievements to reflect the candidate's impact.
        - Start bullet points with action verbs like "Developed," "Implemented," "Managed," "Optimized," and "Achieved" to make the resume more engaging and ATS-readable.
        - Examples of quantitative achievements to use or adapt:
        - "Led a cross-functional team to implement predictive analytics, achieving 90% accuracy in forecasting key metrics and reducing decision-making time by 40% across departments."
        - "Spearheaded a digital transformation initiative that reduced operational costs by 30% and improved process efficiency by 50% within the first 6 months."
        - "Developed a customer segmentation strategy that increased retention rates by 20% and drove a 15% increase in upsell revenue year-over-year."
        - "Redesigned core product architecture, reducing load times by 60% and increasing customer satisfaction scores from 4.2 to 4.9 within one quarter."
        - "Launched an international marketing campaign that expanded brand reach by 200% and achieved a 150% return on investment within 4 months."
        - "Built a scalable data infrastructure that decreased data processing time by 70%, enabling real-time analytics and improving data-driven decision-making."
        - "Reduced employee turnover by 45% through implementing targeted engagement programs, increasing overall employee satisfaction scores by 35%."
        - "Directed sales strategy that exceeded revenue targets by 30% over 3 consecutive quarters, bringing in $15 million in additional revenue."
        - "Improved project delivery timelines by 25% through agile project management, consistently delivering complex projects on time and under budget."
        - "Developed a comprehensive cybersecurity framework, reducing security incidents by 80% and achieving compliance with industry standards within 6 months."

        #### 3. **Error and Typo Correction**
        - Carefully proofread for any typographical errors, grammar issues, or inconsistent formatting that may affect professionalism.
        - Rephrase any awkward phrasing or ambiguous terms to improve clarity and readability. Use grammar-checking tools to catch any mistakes.
        - Common errors to look out for:
        - Spelling mistakes (e.g., "managment" instead of "management")
        - Grammatical errors (e.g., "I have been working at the company for 5 years ago" instead of "I have been working at the company for 5 years")
        - Formatting inconsistencies (e.g., using inconsistent fonts or spacing)

        #### 4. **Keyword and Skill Integration**
        - Analyze the job role(s) the candidate is targeting to identify relevant keywords and integrate them naturally into the CV.
        - Emphasize high-demand skills and qualifications to increase ATS ranking, including both hard and soft skills relevant to the role. Ensure to include both long-form versions and acronym versions of keywords (e.g., "certified public accountant" and "CPA").
        - Tailor the CV to each job application by incorporating relevant keywords from the job description. This may involve tweaking existing keywords to match those in the job description exactly.

        #### 5. **Final Optimized Version of the CV**
        - Provide an improved, finalized ATS-friendly version of the CV.
        - Ensure the CV maintains a clean, minimalistic style that enhances readability while highlighting key achievements.

        #### 6. **Summary of Key Improvements Made**
        - List all major improvements, such as formatting changes, keyword additions, quantifiable results, typo corrections, or any other updates that enhance ATS compatibility and readability.

        #### 7. **Additional Suggestions**
        - Recommend additional changes that could make the CV stand out, such as adding certifications, clarifying job titles to align with industry norms, or updating project descriptions to reflect the latest relevant skills.
        - Suggest a professional email address and ensure contact information is easily visible and up-to-date.
        - For the personal projects section, provide detailed descriptions that emphasize the candidate's technical skills, problem-solving abilities, and the impact of their contributions, without using quantitative metrics.

        ### Final Check
        Before submitting the CV, test it through an ATS simulator or an online resume parser to ensure it performs well in an automated screening process. Make necessary adjustments based on the results to improve compatibility and performance.

        ### Original CV
        {cv_text}
    """

    response = model.generate_content(prompt)
    return response.text

def improve_cv_specific(cv_text, job_description, minimum_qualification):
    # First, improve the CV generally
    improved_cv = improve_cv_general(cv_text)
    
    # Then, tailor it for the specific job description
    prompt = f"""
    As an ATS (Applicant Tracking System) and CV enhancement expert, please review the following improved CV and further optimize it for the specific job description provided. Ensure that the CV is tailored to match the job requirements while maintaining its ATS-friendly format.

    ### Job Description:
    {job_description}

    ### Minimum Qualification:
    {minimum_qualification}

    ### Improved CV:
    {improved_cv}

    Please provide:
    1. A version of the CV tailored specifically for this job description, highlighting relevant skills and experiences.
    2. A list of key changes made to align the CV with the job description.
    3. Additional suggestions for making the CV stand out for this particular role.
    """

    response = model.generate_content(prompt)
    return response.text

st.title("ATS-Friendly CV Improver")

st.subheader("Upload your CV (PDF format):")
pdf_file = st.file_uploader("Choose a PDF file", type="pdf")

if pdf_file is not None:
    with st.spinner("Extracting text from PDF..."):
        cv_text = extract_text_from_pdf(pdf_file)

    st.text_area("Extracted CV Text:", value=cv_text, height=300, key="cv_text_area")

    option = st.selectbox("Choose an option:", ("General CV Enhancement", "Specific Job Description Enhancement"))

    if option == "General CV Enhancement":
        if st.button("Improve CV"):
            with st.spinner("Improving your CV..."):
                improved_cv = improve_cv_general(cv_text)
                st.subheader("Improved CV and Suggestions:")
                st.write(improved_cv)
    else:
        job_description = st.text_area("Enter the job description:", height=150)
        minimum_qualification = st.text_area("Enter the minimum qualification:", height=50)
        if st.button("Improve CV for Specific Job"):
            if job_description and minimum_qualification:
                with st.spinner("Improving your CV for the specific job..."):
                    improved_cv = improve_cv_specific(cv_text, job_description, minimum_qualification)
                    st.subheader("Improved CV and Suggestions for Specific Job:")
                    st.write(improved_cv)
            else:
                st.warning("Please enter both job description and minimum qualification.")

st.sidebar.header("About")
st.sidebar.info(
    "This app uses Google's Gemini AI to improve your CV and make it more ATS-friendly. "
    "Upload your CV in PDF format and choose between general enhancement or tailoring for a specific job description."
)