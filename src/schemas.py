from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal

class SecurityAnalysis(BaseModel):
    attack_type: Literal[
        "SQL Injection",
        "XSS",
        "Path Traversal",
        "Brute Force",
        "Benign", 
        "Unknown"
        ]
    severity: Literal[
        "Low",
        "Medium",
        "High",
        "Critical",
        "Unknown"
    ]
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Estimated confidence between 0 and 1"
        )
    explanation: str = Field(
        ...,
        description="Explanation grounded in the HTTP log"
    )

    evidence: list[str] = Field(
        ...,
        description="List of evidence items supporting the security analysis"
        )

    recommended_action: str = Field(
        ...,
        description="Recommended action to mitigate the identified security issue"
    )

