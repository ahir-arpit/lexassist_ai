import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = []
    
    # Mapping for clearer labels
    label_map = {
        "ORG": "Organization",
        "PERSON": "Legal Party",
        "DATE": "Compliance Date",
        "MONEY": "Financial Clause",
        "GPE": "Jurisdiction",
        "LAW": "Statutory Reference"
    }

    for ent in doc.ents:
        if ent.label_ in label_map:
            entities.append({
                "text": ent.text,
                "type": label_map.get(ent.label_, ent.label_)
            })

    # Return unique entities to keep table clean
    seen = set()
    unique_entities = []
    for e in entities:
        if e['text'] not in seen:
            unique_entities.append(e)
            seen.add(e['text'])
            
    return unique_entities