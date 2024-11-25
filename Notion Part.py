import streamlit as st
import requests
from datetime import datetime, timezone

# Notion API Config
NOTION_TOKEN = "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"
DATABASE_ID = "1494d66e48f480828afeed2595d52910"
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_page(name, description, tags, github_link):
    """Create a new page in the Notion database."""
    create_url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": name}}]},
            "Description": {"rich_text": [{"text": {"content": description}}]},
            "Tags": {"multi_select": [{"name": tag} for tag in tags]},
            "GitHub Link": {"url": github_link},
        },
    }
    response = requests.post(create_url, headers=headers, json=payload)
    return response

def fetch_pages():
    """Fetch all projects from the Notion database."""
    query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"page_size": 100}
    response = requests.post(query_url, headers=headers, json=payload)
    data = response.json()
    return data.get("results", [])

st.title("AIROST Project Management Dashboard")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["View Projects", "Add Project"])

if menu == "View Projects":
    st.subheader("All Projects")
    projects = fetch_pages()
    for project in projects:
        props = project["properties"]
        name = props["Name"]["title"][0]["text"]["content"]
        description = props.get("Description", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "No description")
        tags = [tag["name"] for tag in props.get("Tags", {}).get("multi_select", [])]
        github_link = props.get("GitHub Link", {}).get("url", "No link")
        st.write(f"### {name}")
        st.write(f"**Description:** {description}")
        st.write(f"**Tags:** {', '.join(tags)}")
        st.write(f"**GitHub Link:** [{github_link}]({github_link})")

elif menu == "Add Project":
    st.subheader("Add New Project")
    name = st.text_input("Project Name")
    description = st.text_area("Description")
    tags = st.text_input("Tags (comma-separated)").split(",")
    github_link = st.text_input("GitHub Link")
    if st.button("Add Project"):
        response = create_page(name, description, tags, github_link)
        if response.status_code == 200:
            st.success("Project added successfully!")
        else:
            st.error(f"Failed to add project: {response.text}")


