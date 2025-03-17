import streamlit as st
import openai
import PyPDF2
import pymupdf
from io import BytesIO
from openai import OpenAI
client = OpenAI()
import streamlit.components.v1 as components

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text_from_pdf(file):
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))

    # Extract text from each page
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()

    return text

def get_css():
    with open('main.css') as f:
        css=f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def header():
    html_file = open("content_header.html", "r", encoding="utf-8")
    html_content = html_file.read()
    components.html(html_content, height=600)

def footer():
    html_file = open("content_footer.html", "r", encoding="utf-8")
    html_content = html_file.read()
    components.html(html_content, height=600)

def main():
    # st.title("IEP Assessment Summarization App")
    # File upload
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt"])

    if uploaded_file is not None:
        # Show processing status
        with st.spinner("Processing file..."):
            if uploaded_file.type == "application/pdf":
            # Extract text from digital PDF
                text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
            # Read text file
                text = uploaded_file.read().decode("utf-8")
            else:
                st.error("Please upload a PDF or text file.")
                return

            # Show success message
            st.success("File processed successfully!")

            # Query input
            query = st.text_area("Enter your query")

            if st.button("Submit"):
            # Send query to OpenAI's language model
                response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a skilled school psychologist and special education teacher with strong experience in the Individualized Education Program (IEP), and in assessing students' special eduction skills, including speech, occupational, behavioral, vision, reading, writing, math and science related proficiencies."},
                    {"role": "user", "content": f"Text: {text}\n\nQuery: {query}"}
                ]
            )

                # Display the response
                st.write(response.choices[0].message.content)

    else:
        st.info("Please upload a file to get started.")


    footer()

if __name__ == "__main__":
    main()
