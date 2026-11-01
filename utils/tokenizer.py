import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from utils.logger import log_calls

for package, path in {
    "stopwords": "corpora/stopwords",
    "punkt": "tokenizers/punkt",
    "punkt_tab": "tokenizers/punkt_tab",
}.items():
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(package, quiet=True)

STOP_WORDS = set(stopwords.words("english"))


@log_calls()
def tokenize(text: str) -> str:
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word not in STOP_WORDS]
    return " ".join(filtered_tokens)
