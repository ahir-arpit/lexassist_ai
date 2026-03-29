import torch
from transformers import AutoTokenizer, AutoModel

model_name = "nlpaueb/legal-bert-base-uncased"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModel.from_pretrained(model_name)

def get_embedding(text):

    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**tokens)

    # Use mean pooling of the last hidden state
    embeddings = outputs.last_hidden_state.mean(dim=1)

    return embeddings.squeeze().tolist()