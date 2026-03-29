def split_sentences(text):

    sentences = text.split(".")

    return [s.strip() for s in sentences if s]