from langchain_core.runnables import RunnableLambda

def validate_evidence(data: dict) -> dict:
    analysis = data["analysis"]
    original_log = data["log"]
    valid = [item for item in analysis.evidence 
             if item and item in original_log]
    