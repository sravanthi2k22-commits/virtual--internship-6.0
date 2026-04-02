import streamlit as st

# Page configuration
st.set_page_config(page_title="log-analytics-monitoring-engine", layout="wide")
st.title("log-analytics-monitoring-engine")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Dashboard", "Settings", "Contact"])

# Home tab
with tab1:
    st.header("Welcome to Home!")
    st.write("This is the home page of the application.")

# Dashboard tab
with tab2:
    st.header("Dashboard")
    try:
        import app  # Make sure app.py is in the same folder as menu.py
    except ModuleNotFoundError:
        st.error("Dashboard module not found. Make sure app.py is in the dashboard folder.")

# Settings tab
with tab3:
    st.header("Settings")
    st.write("Settings page.")
    language = st.selectbox("Language", ["English", "Hindi", "Telugu"])

# Contact tab
with tab4:
    st.header("Contact page")
    st.write("Fill the details")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    if st.button("Submit"):
        st.success(f"Thanks {name}, we'll contact you at {email}!")
