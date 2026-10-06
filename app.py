import os

import streamlit as st

from dotenv import load_dotenv
from google import genai

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ============================================================
# SETUP
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY is missing in the .env file.")
    st.stop()


client = genai.Client(
    api_key=GEMINI_API_KEY
)

MODEL = "gemini-3.8-flash"

FILE_SEARCH_STORE_NAME = (
    "fileSearchStores/ai-investment-analysis-35a7218mgjkj"
)

DRIVE_FOLDER_ID = "16f8bYqRFyzL3-eNFY2XL9FrmtI8K61ar"

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]


# ============================================================
# GOOGLE DRIVE AUTHENTICATION
# ============================================================

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

    creds = flow.run_local_server(
        port=0
    )

    with open(
        "token.json",
        "w",
        encoding="utf-8"
    ) as token:

        token.write(
            creds.to_json()
        )


drive = build(
    "drive",
    "v3",
    credentials=creds
)


# ============================================================
# GET DRIVE DOCUMENT LINK
# ============================================================

def get_drive_link(file_name):

    result = drive.files().list(
        q=(
            f"'{DRIVE_FOLDER_ID}' in parents "
            f"and name='{file_name}' "
            "and trashed=false"
        ),
        fields="files(id,name,webViewLink)",
        pageSize=1
    ).execute()

    files = result.get(
        "files",
        []
    )

    if files:

        return files[0].get(
            "webViewLink",
            ""
        )

    return ""


# ============================================================
# FILE SEARCH
# ============================================================

def search_index(question):

    prompt = f"""
You are a financial document assistant.

The financial documents are already indexed in the
Gemini File Search Store.

USER QUESTION:
{question}

Answer the user's question using ONLY the indexed
financial documents.

Rules:

- Search the indexed documents for the relevant information.
- Retrieve only the information needed for the answer.
- Do not use outside knowledge.
- Do not guess.
- Do not invent values.
- Do not mix companies.
- Do not mix reporting periods.
- If the question asks "why", search for the actual
  explanation in the indexed documents, not only the number.
- If multiple pieces of information are required,
  search for all of them before answering.
- If the information is not available, say exactly:

This information is not available in the uploaded documents.

Give a brief and direct answer.

USER QUESTION:
{question}
"""


    interaction = client.interactions.create(
        model=MODEL,
        input=prompt,
        tools=[
            {
                "type": "file_search",
                "file_search_store_names": [
                    FILE_SEARCH_STORE_NAME
                ]
            }
        ]
    )


    answer_parts = []
    sources = []


    for step in interaction.steps:

        if step.type != "model_output":
            continue


        for content_block in step.content:

            if content_block.type != "text":
                continue


            if content_block.text:

                answer_parts.append(
                    content_block.text
                )


            annotations = getattr(
                content_block,
                "annotations",
                None
            )

            if not annotations:
                continue


            for annotation in annotations:

                if annotation.type != "file_citation":
                    continue


                source = {
                    "file_name": getattr(
                        annotation,
                        "file_name",
                        ""
                    ),
                    "source": getattr(
                        annotation,
                        "source",
                        ""
                    )
                }


                if source not in sources:

                    sources.append(
                        source
                    )


    return {
        "answer": "\n".join(
            answer_parts
        ).strip(),
        "sources": sources
    }


# ============================================================
# UI
# ============================================================

page = st.sidebar.radio(
    "Go to",
    [
        "AI Chat",
        "Dashboard"
    ]
)


# ============================================================
# AI CHAT
# ============================================================

if page == "AI Chat":

    st.title(
        "AI Financial Assistant"
    )


    question = st.text_input(
        "Ask a question"
    )


    if st.button(
        "Ask Gemini"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

            st.stop()


        with st.spinner(
            "Searching indexed documents..."
        ):

            try:

                result = search_index(
                    question.strip()
                )


                st.subheader(
                    "Answer"
                )

                st.write(
                    result["answer"]
                )


                if result["sources"]:

                    st.subheader(
                        "Sources"
                    )


                    shown_sources = set()


                    for source in result["sources"]:

                        file_name = source.get(
                            "file_name",
                            ""
                        )


                        if not file_name:
                            continue


                        if file_name in shown_sources:
                            continue


                        shown_sources.add(
                            file_name
                        )


                        drive_link = get_drive_link(
                            file_name
                        )


                        if drive_link:

                            st.markdown(
                                f"[{file_name}]"
                                f"({drive_link})"
                            )

                        else:

                            st.write(
                                file_name
                            )


            except Exception as error:

                st.error(
                    "File Search failed."
                )

                st.exception(
                    error
                )


# ============================================================
# DASHBOARD
# ============================================================

else:

    st.title(
        "Dashboard"
    )

    st.info(
        "Dashboard is separate from the File Search based AI Chat flow."
    )