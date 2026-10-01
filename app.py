import os
import json
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing in the .env file.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)

# ===== LOAD FILE REGISTRY (Pre-connected documents) =====
try:
    with open("file_registry.json", "r") as f:
        file_registry = json.load(f)
except FileNotFoundError:
    st.error("file_registry.json not found. Run upload_documents.py first!")
    st.stop()

# ===== UI =====
st.title("📊 AI Financial Analysis")

# Show which companies are available
companies_list = list(file_registry["companies"].keys())
company_names = {key: file_registry["companies"][key]["name"] for key in companies_list}

# User selects company
selected_company = st.selectbox(
    "Select Company",
    companies_list,
    format_func=lambda x: company_names[x]
)

# User asks question
question = st.text_input("Ask a question about the documents")

# Ask Gemini
if st.button("Ask Gemini"):
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Analyzing documents..."):
        try:
            # Get file IDs for selected company
            company_docs = file_registry["companies"][selected_company]["documents"]
            
            # Get file objects from Gemini using stored IDs
            gemini_files = []
            doc_names = []
            
            for doc_type, doc_info in company_docs.items():
                file_id = doc_info["file_id"]
                file_obj = client.files.get(name=file_id)
                gemini_files.append(file_obj)
                doc_names.append(doc_info["original_filename"])

            # Create prompt
            prompt = f"""
You are a Senior Financial Analyst AI.

You are analyzing financial documents for: {company_names[selected_company]}

Documents available:
{', '.join(doc_names)}

RULES:
1. Answer ONLY using information from the provided documents
2. Never guess or use outside information
3. Always cite the source (document name and page number)
4. Be precise with numbers and dates

User question:
{question}



Provide:
1. Direct answer
2. Source citation (document name, page number)
3. Any relevant context from the documents
"""

            # Call Gemini with pre-loaded files
            contents = gemini_files + [prompt]
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=contents,
            )

            # Display answer
            st.subheader("Answer")
            st.write(response.text)

        except Exception as error:
            st.error(f"Error: {error}")