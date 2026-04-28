import sqlite3
import pandas as pd
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="NL → SQL Analytics Demo", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("NL → SQL Analytics Demo")
st.write("Ask a business question. The app translates it into SQL, runs it, and summarizes the result.")

# Sample data
data = pd.DataFrame({
    "sku": ["A100", "A100", "B200", "B200", "C300", "C300"],
    "region": ["CA", "NV", "CA", "NV", "CA", "NV"],
    "week": ["2026-01-01", "2026-01-01", "2026-01-08", "2026-01-08", "2026-01-15", "2026-01-15"],
    "revenue": [12000, 9000, 8500, 11000, 6000, 14000],
    "units_sold": [120, 90, 85, 110, 60, 140],
    "forecast": [13000, 9500, 9000, 10000, 8000, 12000],
    "customer_type": ["Retail", "Retail", "Wholesale", "Retail", "Wholesale", "Wholesale"]
})

conn = sqlite3.connect(":memory:")
data.to_sql("sales", conn, index=False, if_exists="replace")

schema = """
Table: sales
Columns:
- sku TEXT
- region TEXT
- week TEXT
- revenue INTEGER
- units_sold INTEGER
- forecast INTEGER
- customer_type TEXT
"""

def generate_sql(question):
    prompt = f"""
You are a data analyst. Convert the user's question into SQLite SQL.

Rules:
- Use only the table and columns below.
- Only generate SELECT statements.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, PRAGMA, or CREATE.
- Return SQL only. No explanation.

{schema}

User question: {question}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text.strip().replace("```sql", "").replace("```", "").strip()

def is_safe_sql(sql):
    blocked = ["insert", "update", "delete", "drop", "alter", "pragma", "create", "attach", "detach"]
    cleaned = sql.lower().strip()
    return cleaned.startswith("select") and not any(word in cleaned for word in blocked)

def summarize_result(question, sql, result_df):
    prompt = f"""
You are an analytics consultant.

User question:
{question}

SQL used:
{sql}

Result:
{result_df.to_string(index=False)}

Summarize the business insight in 2-4 sentences.
Mention any caveats.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text.strip()

question = st.text_input("Ask a question:", placeholder="Which region is underperforming forecast?")

if st.button("Run Analysis") and question:
    sql = generate_sql(question)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    if not is_safe_sql(sql):
        st.error("Unsafe SQL blocked. Only SELECT queries are allowed.")
    else:
        try:
            result = pd.read_sql_query(sql, conn)

            st.subheader("Query Result")
            st.dataframe(result, use_container_width=True)

            st.subheader("AI Summary")
            summary = summarize_result(question, sql, result)
            st.write(summary)

        except Exception as e:
            st.error(f"Query failed: {e}")
