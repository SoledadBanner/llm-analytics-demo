import streamlit as st

st.title("LLM Analytics Demo")

query = st.text_input("Ask a question about your data:")

if query:
    st.write("Simulated response for:", query)
