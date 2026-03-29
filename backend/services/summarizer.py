from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def generate_summary(text):

    summary = summarizer(
        text[:2000],
        max_length=300,
        min_length=120,
        do_sample=False
    )

    return summary[0]["summary_text"]