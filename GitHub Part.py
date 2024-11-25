import requests
import streamlit as st

GITHUB_TOKEN = "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"
GITHUB_REPO = "OwenAw/AIROST-Knowledge-Base" 

def fetch_files_from_github():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        files = response.json()
        return files
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return []

def display_files_in_dashboard(files):
    st.title("Project Files")
    for file in files:
        st.markdown(f"- [{file['name']}]({file['html_url']})")

files = fetch_files_from_github()
if files:
    display_files_in_dashboard(files)
else:
    st.warning("No files found or failed to fetch data.")
