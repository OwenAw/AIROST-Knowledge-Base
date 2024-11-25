import streamlit as st
import requests

# Configuration
NOTION_TOKEN = "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"
DATABASE_ID = "1494d66e48f480828afeed2595d52910"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Fetch filtered pages
def fetch_filtered_pages(search_text=None, tag_filter=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    filters = []

    if tag_filter:
        filters.append({
            "property": "Tags",
            "multi_select": {"contains": tag_filter}
        })

    if search_text:
        filters.append({
            "property": "Name",
            "title": {"contains": search_text}
        })

    payload = {"filter": {"and": filters}} if filters else {}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        print("Error fetching projects:", response.status_code, response.text)
        response.raise_for_status()
    
    results = response.json()["results"]
    projects = []
    for result in results:
        try:
            project_title = result["properties"]["Name"]["title"][0]["text"]["content"]
            project_tags = [tag["name"] for tag in result["properties"].get("Tags", {}).get("multi_select", [])]
            project_url = result["properties"].get("GitHub Link", {}).get("url", "No link")  # Fetch the project URL from the metadata
            projects.append({
                "title": project_title,
                "tags": project_tags,
                "url": project_url
            })
        except KeyError as e:
            print(f"Missing property: {e}")
    return projects

# Display the app
def display_projects():
    st.title("Searchable Knowledge Base")
    
    search_text = st.text_input("Search by Title")
    tag_filter = st.selectbox("Search by Tag:", ["AI", "Robotics", "IoT", ""])

    if st.button("Search"):
        try:
            projects = fetch_filtered_pages(search_text=search_text, tag_filter=tag_filter)
            if projects:
                for project in projects:
                    st.subheader(project["title"])
                    st.write(f"Tags: {', '.join(project['tags'])}")
                    st.markdown(f"[View Project]({project['url']})")  # Create a clickable URL link
                    st.write("---")
            else:
                st.write("No projects found.")
        except Exception as e:
            st.error(f"Error fetching projects: {e}")

# Main app
if __name__ == "__main__":
    display_projects()
