import asyncio
from paperqa import Docs
from paperqa.settings import Settings
from paperqa.sources.clinical_trials import add_clinical_trials_to_docs

async def run_trial_query(question: str, limit: int = 5):
    docs = Docs()
    settings = Settings()

    await add_clinical_trials_to_docs(
        query=question,
        docs=docs,
        settings=settings,
        limit=limit,
    )

    return await docs.aquery(question)

def run(question: str, limit: int = 5):
    return asyncio.run(run_trial_query(question, limit))