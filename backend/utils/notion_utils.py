# utils/notion_utils.py

from notion_client import Client
from urllib.parse import urlparse
import requests

# --- EXISTING FUNCTIONS ---

# ✅ Extract page ID from URL (FIXED)
def get_page_id_from_url(url: str) -> str:
    # 1. Parse the URL to get the path part
    parsed_url = urlparse(url)
    
    # 2. Extract the part containing the ID, handling both hyphenated and unhyphenated IDs
    # Find the last 32 characters, which should be the unhyphenated ID
    id_match = None
    
    # Clean the path: remove page title, hyphens, and any query params
    # Example path: /STuPA-Portfolio-Data-698267856f734c55b0f82bb97f8a5062
    path_without_hyphens = parsed_url.path.replace('-', '')
    
    # The page ID is the last 32 hex characters in the path
    id_match = path_without_hyphens[-32:]
    
    # 3. Validation: Ensure the extracted string is a 32-character hex string
    if len(id_match) != 32 or not all(c in '0123456789abcdef' for c in id_match.lower()):
        # This will catch the previous error where an invalid ID was generated
        raise ValueError(f"Invalid Notion page ID extracted from URL: {id_match}")
        
    return id_match

# ✅ Fetch all child databases (No change needed here; it looks correct)
def get_child_databases(token: str, page_id: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # The Notion API accepts unhyphenated IDs for blocks/pages
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # Include the full response text for better debugging
        raise Exception(f"Error {response.status_code}: {response.text}")

    data = response.json()

    db_dict = {}
    for result in data.get("results", []):
        if result["type"] == "child_database":
            db_dict[result["child_database"]["title"]] = result["id"]

    return db_dict


# --- NEW REQUIRED FUNCTIONS ---

# ✅ Fetch all pages/rows from a database (NEW)
def query_database_pages(token: str, database_id: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    # We use a POST request to query a database
    response = requests.post(url, headers=headers, json={})

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    data = response.json()
    
    return data.get("results", [])


# ✅ Helper function to clean raw Notion properties (NEW)

def clean_notion_properties(page_properties: dict) -> dict:
    """
    Takes raw Notion page properties and extracts clean values.
    This is necessary because Notion's API wraps every value in nested objects.
    """
    clean_data = {}
    for key, prop in page_properties.items():
        prop_type = prop["type"]
        
        # Determine the value based on property type
        if prop_type == "title":
            value = prop["title"][0]["plain_text"] if prop["title"] else ""
        elif prop_type == "rich_text":
            value = prop["rich_text"][0]["plain_text"] if prop["rich_text"] else ""
        elif prop_type == "number":
            value = prop["number"]
        elif prop_type == "url":
            value = prop["url"]
        elif prop_type == "multi_select":
            value = [item["name"] for item in prop["multi_select"]]
        elif prop_type == "select":
            value = prop["select"]["name"] if prop["select"] else None
        elif prop_type == "checkbox":
            value = prop["checkbox"]
        else:
            # For unsupported types (like files, relations), return the raw value
            value = prop.get(prop_type, None)

        # Standardize key names (e.g., "Project Name" -> "project_name")
        clean_data[key.lower().replace(" ", "_")] = value
        
    return clean_data
