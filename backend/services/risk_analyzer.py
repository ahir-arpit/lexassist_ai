import re

# Risk categories with weights and alternative patterns
RISK_DATABASE = [
    {
        "id": "non_compete",
        "label": "Non-Compete Clause",
        "weight": 35,
        "patterns": ["non-compete", "non compete", "restraint of trade", "exclusivity"]
    },
    {
        "id": "termination",
        "label": "Unfair Termination",
        "weight": 25,
        "patterns": ["terminate without notice", "instant termination", "30 days notice", "notice period"]
    },
    {
        "id": "penalty",
        "label": "Heavy Penalties",
        "weight": 20,
        "patterns": ["penalty", "fine", "liquidated damages", "compensation for breach"]
    },
    {
        "id": "liability",
        "label": "Unlimited Liability",
        "weight": 20,
        "patterns": ["unlimited liability", "full responsibility", "indemnify and hold harmless"]
    }
]

def analyze_risk(text: str):
    text_normalized = text.lower()
    detected_ids = []
    detected_labels = []
    total_score = 0
    
    for risk in RISK_DATABASE:
        found = False
        for pattern in risk["patterns"]:
            if pattern in text_normalized:
                found = True
                break
        
        if found:
            detected_ids.append(risk["id"])
            detected_labels.append(risk["label"])
            total_score += risk["weight"]
            
    # Cap score at 100
    total_score = min(total_score, 100)
    
    # Accurate Thresholds based on typical legal demo standards
    if total_score >= 60:
        level = "High"
    elif total_score >= 30:
        level = "Medium"
    else:
        level = "Low"
        
    return {
        "risk_score": total_score,
        "risk_level": level,
        "detected_clauses": detected_labels
    }