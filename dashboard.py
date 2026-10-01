import streamlit as st


def show_dashboard(drive, folder_id):

    st.title("Investment Dashboard")

    result = drive.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id,name,mimeType,size,modifiedTime)"
    ).execute()

    files = result.get("files", [])

    if not files:
        st.warning("No files found in Google Drive.")
        return

    st.subheader("Connected Documents")

    for file in files:
        file_id = file["id"]

        data = drive.files().get_media(
            fileId=file_id
        ).execute()

        st.write(file["name"])

        st.write(f"PDF size: {len(data)} bytes")

        st.divider()