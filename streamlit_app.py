# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

#credentials = service_account.Credentials.from_service_account_info(
              #  st.secrets["gcp_service_account"], scopes = scope)
#client = Client(scope=scope,creds=credentials)
#spreadsheetname = Database
#spread = Spread(spreadsheetname)

# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=60)

# Perform SQL query on the Google Sheet.
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(f"{row.Acronym} has a :{row.Definition}:")
