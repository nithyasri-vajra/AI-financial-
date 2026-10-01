import os
import streamlit as st

from dotenv import load_dotenv
from google import genai

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dashboard import show_dashboard

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing in the .env file.")
    st.stop()


client = genai.Client(api_key=api_key)

DRIVE_FOLDER_ID = "16f8bYqRFyzL3-eNFY2XL9FrmtI8K61ar"

# Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )
else:
    flow = InstalledAppFlow.from_client_secrets_file(
        "finanicial-drive-credential.json",
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())


drive = build(
    "drive",
    "v3",
    credentials=creds
)


# UI
page = st.sidebar.radio(
    "Go to",
    ["AI Chat", "Dashboard"]
)

if page == "AI Chat":

    question = st.text_input(
        "Ask a question"
    )


    if st.button("Ask Gemini"):

        if not question.strip():
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner("Reading financial documents..."):

            try:

                # Get PDFs from Drive
                results = drive.files().list(
                    q=f"'{DRIVE_FOLDER_ID}' in parents and "
                    "mimeType='application/pdf' and trashed=false",
                    fields="files(id,name,webViewLink)"
                ).execute()

                files = results.get("files", [])

                if not files:
                    st.error(
                        "No PDF documents found in Google Drive."
                    )
                    st.stop()


                # Download PDF contents
                document_parts = []

                for drive_file in files:

                    data = drive.files().get_media(
                        fileId=drive_file["id"]
                    ).execute()

                    temp_path = f"temp_{drive_file['id']}.pdf"

                    with open(temp_path, "wb") as f:
                        f.write(data)


                    gemini_file = client.files.upload(
                        file=temp_path,
                        config={
                            "mime_type": "application/pdf",
                            "display_name": drive_file["name"]
                        }
                    )

                    document_parts.append(gemini_file)

                    os.remove(temp_path)


                prompt = f"""
    You are an AI financial document analysis assistant.

    Search ALL provided financial PDF documents before answering.

    The user gives only a question. The user may not tell you the company,
    document, report, period, or page.

    Identify the correct document yourself.

    Use ONLY information from the provided PDFs.

    Do not guess.
    Do not use outside information.
    Do not mix companies or reporting periods.

    If the question requires multiple documents, use all relevant documents.

    If the information cannot be found, say:

    "This information is not available in the uploaded documents."

    Answer only what the user asked.

    User question:
    {question}
    """


                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=document_parts + [prompt]
                )


                st.subheader("Answer")
                st.write(response.text)


            except Exception as error:
                st.error(
                    "Something went wrong while analyzing "
                    "the documents."
                )

                st.code(str(error))

else:
    show_dashboard(drive, DRIVE_FOLDER_ID)