import asyncio
import requests
from paperqa import Docs
from paperqa.settings import Settings
from paperqa.sources.clinical_trials import add_clinical_trials_to_docs

# --- Main PaperQA query ---
def answer_question(question: str, k: int = 5):
    """Uses ClinicalTrials.gov search and returns LLM answer via PaperQA."""
    docs = Docs()
    settings = Settings()

    async def run():
        await add_clinical_trials_to_docs(
            query=question,
            docs=docs,
            settings=settings,
            limit=k
        )
        return await docs.aquery(question)

    return asyncio.run(run())

# --- Fallback API query using original user question ---
def fallback_clinical_trials_api(question: str, max_results: int = 10):
    """Query ClinicalTrials.gov directly using the raw user question."""
    base_url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": question,
        "fields": "NCTId,BriefTitle,Condition,Phase,OverallStatus,LocationCountry",
        "min_rnk": 1,
        "max_rnk": max_results,
        "fmt": "json"
    }

    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()["StudyFieldsResponse"]["StudyFields"]

# --- Smart wrapper: Try PaperQA first, fallback to API if it fails or is empty ---
def smart_answer_question(question: str, k: int = 5):
    try:
        result = answer_question(question, k)
        # Check if sources exist or fallback needed
        if hasattr(result, "sources") and result.sources:
            return result
        else:
            fallback = fallback_clinical_trials_api(question, max_results=k)
            return {"fallback": True, "results": fallback}
    except Exception as e:
        fallback = fallback_clinical_trials_api(question, max_results=k)
        return {"fallback": True, "results": fallback, "error": str(e)}