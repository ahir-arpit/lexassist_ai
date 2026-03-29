from typing import List, Dict

# Mapping of contract keywords/concepts to Indian Contract Act (ICA) sections
ICA_MAPPINGS = [
    {
        "concept": "Restraint of Trade / Non-Compete",
        "keywords": ["non-compete", "restraint of trade", "exclusivity", "non compete"],
        "section": "Section 27",
        "detail": "Agreements in restraint of trade are void, except for cases of goodwill of a business.",
        "risk_impact": "High - May be legally unenforceable in India."
    },
    {
        "concept": "Liquidated Damages / Penalty",
        "keywords": ["penalty", "liquidated damages", "compensation for breach"],
        "section": "Section 74",
        "detail": "Compensation for breach of contract where a penalty is stipulated for.",
        "risk_impact": "Medium - Courts may only award 'reasonable compensation' regardless of the specified amount."
    },
    {
        "concept": "Nature of Breach / Damages",
        "keywords": ["damages", "loss", "injury", "liability"],
        "section": "Section 73",
        "detail": "Compensation for loss or damage caused by breach of contract.",
        "risk_impact": "Medium - Damages must be proximity-based and not remote."
    },
    {
        "concept": "Force Majeure / Frustration",
        "keywords": ["force majeure", "act of god", "unforeseen", "impossible"],
        "section": "Section 56",
        "detail": "Agreement to do impossible acts; contract becomes void if acts become impossible.",
        "risk_impact": "Medium - Standard protection, but interpretation varies."
    },
    {
        "concept": "Capacity of Parties",
        "keywords": ["minor", "sound mind", "competent"],
        "section": "Section 11",
        "detail": "Who are competent to contract (Age of majority, sound mind).",
        "risk_impact": "High - Fundamental validity of the agreement."
    }
]

def compare_with_law(text: str) -> List[Dict]:
    text_lower = text.lower()
    comparisons = []
    
    for entry in ICA_MAPPINGS:
        found = False
        for kw in entry["keywords"]:
            if kw in text_lower:
                found = True
                break
        
        if found:
            comparisons.append({
                "concept": entry["concept"],
                "section": entry["section"],
                "legal_provision": entry["detail"],
                "compliance_note": entry["risk_impact"]
            })
            
    # If no specific matches, provide a general citation
    if not comparisons:
        comparisons.append({
            "concept": "General Compliance",
            "section": "Section 10",
            "legal_provision": "All agreements are contracts if they are made by free consent of parties competent to contract.",
            "compliance_note": "Ensures basic contractual validity."
        })
        
    return comparisons
