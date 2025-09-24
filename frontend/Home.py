import streamlit as st
import requests
st.set_page_config(page_title="CloudJune Social Support - Demo", layout="wide")

st.title("CloudJune Social Support — Prototype Demo")

st.markdown("""
This demo shows:
- Uploading a file (CSV or Excel) to the backend ingest endpoint.
- Running a mock eligibility prediction.
- A simple chatbot that returns canned responses.
""")

with st.expander("Upload / Ingest Example"):
    uploaded = st.file_uploader("Upload a CSV or Excel file", type=['csv','xls','xlsx'])
    if uploaded is not None:
        files = {'file': (uploaded.name, uploaded.getvalue())}
        resp = requests.post("http://localhost:8000/ingest/upload", files=files)
        st.write("Ingest response:")
        st.json(resp.json())

with st.expander("Eligibility Checker"):
    income = st.number_input("Monthly Income (AED)", min_value=0.0, value=3000.0)
    family_size = st.number_input("Family size", min_value=1, value=3)
    employment_years = st.number_input("Employment years", min_value=0.0, value=2.0)
    assets = st.number_input("Assets value (AED)", min_value=0.0, value=500.0)
    if st.button("Run Eligibility Check"):
        payload = {'income': income, 'family_size': family_size, 'employment_years': employment_years, 'assets_value': assets}
        resp = requests.post("http://localhost:8000/eligibility/predict", json=payload)
        st.write("Eligibility result:")
        st.json(resp.json())

with st.expander("Chatbot Demo"):
    q = st.text_input("Ask the chatbot for guidance", value="What training should I do?")
    if st.button("Ask"):
        resp = requests.post("http://localhost:8000/chatbot/ask", json={'message': q})
        st.write(resp.json())