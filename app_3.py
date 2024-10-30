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
        As an ATS (Applicant Tracking System) and CV enhancement expert, please thoroughly review the following CV and optimize it for ATS compatibility. Pay special attention to any issues that could affect ATS parsing, including formatting, keyword relevance, and especially the use of quantifiable achievements in the experience section. If any job descriptions lack quantifiable data, modify them to include quantifiable achievements or responsibilities, indicating estimated metrics with brackets, e.g., [5%].

        ### Instructions for Optimization

        #### 1. **Correct Formatting and Layout for ATS Compatibility**
        - Ensure the CV has a simple, ATS-friendly layout (no tables, graphics, or complex formatting).
        - Use a consistent font and spacing style throughout the CV. Recommended fonts include Arial, Calibri, or Times New Roman, with a font size between 10 and 12 points.
        - Organize sections clearly with appropriate headings like "Experience," "Education," and "Skills" for easy ATS reading. Use bold or larger font for these headings to enhance readability.

        #### 2. **Experience Section - Quantitative Enhancements**
        - In the experience section, ensure each job description includes specific, measurable achievements or responsibilities reflecting the candidate's impact. If no quantifiable information is provided, revise descriptions to add quantitative aspects, using placeholders in brackets where necessary (e.g., [5%]).
        - Ensure that every job description in the experience section is either a quantifiable achievement or a quantifiable responsibility.
        - Start bullet points with action verbs like "Developed," "Implemented," "Managed," "Optimized," and "Achieved" to make the resume more engaging and ATS-readable.
        - Examples of quantitative achievements to use or adapt:
        - "Identification and implementation of [5%] cost-saving measures, resulting in increased efficiency and reduced expenses."
        - "Development and execution of [20%] increase in sales strategy, leading to significant revenue growth."
        - "Redesign of [30%] more efficient workflow process, resulting in improved productivity and reduced errors."

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
        - For the personal projects section, provide detailed descriptions that emphasize the candidate's quantify technical skills, problem-solving abilities, and the impact of their contributions.

        #### 8. **ATS-Friendly Section Headings**
        - Use ATS-friendly section headings, such as "Experience," "Education," "Skills," and "Certifications," to help the ATS system accurately parse and categorize the CV.
        - Avoid using creative or non-standard section headings, as they may confuse the ATS system.

        #### 9. **Keyword Density and Placement**
        - Analyze the keyword density and placement throughout the CV to ensure that relevant keywords appear frequently enough to pass the ATS filter.
        - Use keywords strategically in the CV, particularly in the experience section, to increase the chances of passing the ATS filter.

        #### 10. **ATS Simulator Testing**
        - Test the CV through an ATS simulator or an online resume parser to ensure it performs well in an automated screening process.
        - Make necessary adjustments based on the results to improve compatibility and performance.

        #### 11. **Use of Bullet Points**
        - Consistently use bullet points to list responsibilities and achievements under each job title. This makes it easier for the ATS to parse and for human readers to scan quickly.

        #### 12. **Contact Information**
        - Place contact information at the top of the CV, including full name, phone number, email address, and LinkedIn profile if applicable. Ensure this information is accurate and professional.

        #### 13. **File Format**
        - Save the CV in a format that is widely accepted and ATS-friendly, such as .docx or .pdf. Avoid using .jpg or .png formats.

        #### 14. **Avoid Special Characters**
        - Avoid using special characters, symbols, or non-standard fonts that may confuse the ATS. Stick to standard characters and symbols.

        #### 15. **Consistent Date Formatting**
        - Use a consistent date format throughout the CV, such as MM/YYYY or Month YYYY, to ensure the ATS can properly read and parse the dates.

        #### 16. **Professional Summary**
        - Include a professional summary or objective statement at the beginning of the CV. This should be a brief paragraph that highlights key skills, experience, and career objectives.

        #### 17. **Relevant Courses and Training**
        - List relevant courses, certifications, and professional development activities in a specific section to show continuous learning and development.

        #### 18. **Technical Skills Section**
        - Create a dedicated section for technical skills, listing programming languages, software tools, and other technical competencies that are relevant to the job.

        #### 19. **Use of Acronyms**
        - Spell out acronyms the first time they are used, followed by the acronym in parentheses. For example, "Certified Public Accountant (CPA)."

        #### 20. **Avoid Industry Jargon**
        - Avoid excessive use of industry jargon that may not be recognized by the ATS. Use clear and straightforward language.

        #### 21. **Use of Hyperlinks**
        - Include hyperlinks to professional profiles, such as LinkedIn, but ensure they are text-based (e.g., "linkedin.com/in/yourprofile") to avoid issues with ATS parsing.

        #### 22. **Education Section**
        - List educational institutions in reverse chronological order, including the degree earned, institution name, and graduation date.

        #### 23. **Professional Development**
        - Highlight any professional development activities, such as conferences, workshops, or webinars, that demonstrate continuous learning and growth.

        #### 24. **Volunteer Work**
        - Include relevant volunteer work in a separate section, emphasizing skills and experiences that are transferable to the job.

        #### 25. **Achievements and Awards**
        - Create a section for achievements and awards, listing any recognition, scholarships, or honors received.

        #### 26. **Publications and Presentations**
        - If applicable, include a section for publications and presentations, highlighting any articles, papers, or presentations that demonstrate expertise in the field.

        #### 27. **Languages**
        - List any additional languages spoken and the level of proficiency in a separate section.

        #### 29. **Customization for Each Job**
        - Tailor the CV for each job application by customizing the summary, keywords, and experiences to match the specific job description.

        #### 30. **Final Review**
        - Conduct a final review of the CV to ensure all sections are complete, formatted consistently, and free of errors. Use spell-check and grammar-check tools for accuracy.

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

    ##st.text_area("Extracted CV Text:", value=cv_text, height=300, key="cv_text_area")

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

