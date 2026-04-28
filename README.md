# LLM Analytics Demo (NABIS)

## Overview
This project demonstrates a lightweight LLM-powered analytics interface that translates natural language questions into structured queries and returns business insights.

## Example Questions
- Which SKUs are declining week over week?
- What regions are underperforming vs forecast?

## How It Works
1. User inputs a natural language question
2. LLM interprets intent and generates query logic
3. Query runs against dataset (Pandas DataFrame)
4. Output returned as summary + data

## Key Features
- Natural language → query translation
- Schema-aware prompting to reduce hallucinations
- Designed for real-world analytics workflows

## Tech Stack
- Python
- Streamlit
- OpenAI API (or similar LLM)
- Pandas

## Next Steps
- Add validation layer for query accuracy
- Introduce conversational memory
- Integrate with BI tools

## Note
This was built as a demo to explore how LLMs can augment analytics workflows.
