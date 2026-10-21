import re
from langchain_core.runnables import RunnableLambda

INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"forget (all )?previous instructions",
    r"system prompt", 
    r"developer message",
    r"you are now", 
    r"override (the )?instructions",
]
 
def detect_prompt_injection(data: dict) -> dict:
    log = data["log"]
    matches = [
        p for p in INJECTION_PATTERNS 
        if re.search(p, log, re.IGNORECASE)
        ]

    return {
        **data,
        "injection_detected" : bool(matches),
        "injection_patterns" : matches
    }

injection_detector = RunnableLambda(detect_prompt_injection)

