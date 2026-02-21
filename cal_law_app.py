
import streamlit as st
import urllib.parse
from datetime import datetime

# --- UI Setup ---
st.set_page_config(page_title="CA Legal Research Pro", page_icon="⚖️", layout="wide")

# --- Initialize Session State for History ---
if 'search_history' not in st.session_state:
    st.session_state['search_history'] = []

# --- Helper Functions ---
def add_to_history(query_str, url):
    """Adds a new search to the top of the history list."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = {"time": timestamp, "query": query_str, "url": url}
    # Insert at the beginning of the list
    st.session_state['search_history'].insert(0, entry)
    # Keep only the last 10 searches
    st.session_state['search_history'] = st.session_state['search_history'][:10]

def get_boolean_string(base_query, area_list):
    if not base_query: return ""
    formatted_query = f'"{base_query}"' if " " in base_query else base_query
    if area_list:
        area_terms = " AND ".join([f'"{area}"' for area in area_list])
        return f"{formatted_query} AND {area_terms}"
    return formatted_query

def build_scholar_url(full_boolean_query, year):
    base_url = "https://scholar.google.com/scholar?"
    params = {"q": full_boolean_query, "hl": "en", "as_sdt": "4,5", "as_ylo": year, "as_vis": "1"}
    return base_url + urllib.parse.urlencode(params)

# --- Sidebar: Research History ---
with st.sidebar:
    st.header("📜 Recent Searches")
    if not st.session_state['search_history']:
        st.write("No searches yet this session.")
    else:
        for idx, item in enumerate(st.session_state['search_history']):
            st.markdown(f"**{item['time']}**")
            st.caption(item['query'])
            st.link_button(f"Re-open Search #{idx+1}", item['url'])
            st.divider()
        
        if st.button("Clear History"):
            st.session_state['search_history'] = []
            st.rerun()

# --- Main Interface ---
st.title("⚖️ CA Supreme & Appellate Search")
st.markdown("Automated research for Law & Motion Attorneys.")

query = st.text_input("Primary Search Terms:", placeholder="e.g., 'privilege log sufficiency'")

col1, col2 = st.columns(2)
with col1:
    areas = st.multiselect("Focus Areas:", ["Tort", "Civil Procedure", "Personal Injury", "Evidence", "Discovery", "Contract", "Employment"])

with col2:
    date_option = st.selectbox("Date Range:", ["All Time", "Last 2 Years", "Last 5 Years", "Last 10 Years", "Custom Year"])
    start_year = ""
    if "Last" in date_option:
        years_back = int(date_option.split()[1])
        start_year = str(datetime.now().year - years_back)
    elif date_option == "Custom Year":
        start_year = st.text_input("Enter Year (YYYY):", value=str(datetime.now().year))

boolean_str = get_boolean_string(query, areas)

if boolean_str:
    st.subheader("📋 Boolean Search String")
    st.code(boolean_str, language="text")
    
    # Logic for searching and saving history
    final_url = build_scholar_url(boolean_str, start_year)
    
    if st.button("Open Results in New Tab ↗️"):
        # Save to history BEFORE opening
        add_to_history(boolean_str, final_url)
        # Use link button for the actual redirect
        st.link_button("Confirm Redirect to Google Scholar", final_url)
