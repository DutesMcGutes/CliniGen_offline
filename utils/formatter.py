# utils/formatter.py

import pandas as pd

def format_answer(answer) -> str:
    """Format the output from Docs.query to be Streamlit-friendly."""
    if hasattr(answer, 'answer'):
        return answer.answer
    return str(answer)

def format_sources(answer):
    """Create a DataFrame from sources if present."""
    if hasattr(answer, 'sources'):
        data = []
        for s in answer.sources:
            entry = {
                "Title": s.metadata.get("title", "No title"),
                "URL": s.url if hasattr(s, 'url') else "No URL"
            }
            data.append(entry)
        return pd.DataFrame(data)
    return pd.DataFrame()
