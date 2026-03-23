import streamlit as st

st.set_page_config(page_title="log-analytics-monitoring-engine ", layout="wide")
st.title("log-analytics-monitoring-engine")
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Dashboard", " Settings", " Contact"])
with tab1:
    st.header("Welcome to Home!")
    st.write("This is the home page of the application.")

with tab2:
    st.header("Dashboard")
    st.write("Dashboard page.")

with tab3:
    st.header("Settings")
    st.write("setting page.")
    language  = st.selectbox("Language", ["English", "Hindi", "Telugu"])
with tab4:
    st.header("Contact page")
    st.write("fill the deatils")
    name  = st.text_input("Your Name")
    email = st.text_input("Your Email")
    if st.button("Submit"):
        st.success(f"Thanks {name}, we'll contact you at {email}!")