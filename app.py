import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LLM Analytics Demo", layout="centered")

st.title("LLM Analytics Demo")
st.write("Ask a business question and get an analytics-style response.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

schema_context = """
Available dataset fields:
- sku
- region
- week
- revenue
- units_sold
- forecast
- customer_type

Only answer using these fields. If the question cannot be answered from this schema, say what data would be needed.
"""

question = st.text_input("Ask a question about the data:")

if st.button("Generate Insight") and question:
    with st.spinner("Analyzing..."):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
You are an analytics assistant.

{schema_context}

User question:
{question}

Respond with:
1. Interpreted business question
2. Suggested analysis approach
3. Example insight
4. Caveats or validation needed
"""
        )

        st.subheader("AI Response")
        st.write(response.output_text)
