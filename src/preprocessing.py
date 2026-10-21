from langchain_core.runnables import Runnable, RunnableConfig, RunnableSequence, RunnableMap, RunnableLambda

def preprocess_log(log: str) -> dict:
    if not isinstance(log, str): #valida que sea un String
        raise TypeError ("The input must be a String")
    
    cleaned_log = log.strip() # Mejorar esta parte con mas operaciones
    
    if not cleaned_log:
        raise ValueError ("The log cannot be empty")
    
    if len (cleaned_log) > 10_000:
        raise ValueError ("Log Exceed maximum length")

    return({
        "log":          cleaned_log,
        "log_length":   len(cleaned_log)
    })