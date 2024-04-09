from sklearn.feature_extraction.text import TfidfVectorizer
import re
from pprint import pprint
from textblob import TextBlob
from sklearn.decomposition import NMF, LatentDirichletAllocation
from services.logging_config import root_logger as logger


def clean_text(text):
    """
    Remove special characters, extra whitespaces, and convert text to lower case.
    """
    if not isinstance(text, str):
        logger.error(f"clean text received non-string input: {type(text) - {text}}")
        return ""
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\b\w*\d\w*\b", "", text)  # Remove words containing numbers
    return text.lower()


def tfidf_transform(corpus):
    """
    Transform a list of documents into their TF-IDF representation.
    """
    vectorizer = TfidfVectorizer(
        max_df=1.0,
        min_df=0.0,
        stop_words="english",
        ngram_range=(1, 2),
        norm="l2",
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=True,
    )
    X = vectorizer.fit_transform(corpus)
    return X, vectorizer.get_feature_names_out()


def text_to_tokens(text, nlp):
    """
    Convert text into a list of tokens using spaCy.
    """
    doc = nlp(text)
    return [token.text for token in doc]


def lemmatize_text(text, nlp):
    """
    Convert words to their base or root form to reduce dimensionality.
    """
    doc = nlp(text)
    lemmatized = " ".join([token.lemma_ for token in doc])
    return lemmatized


def extract_entities(text, nlp):
    """
    NER for extracting names, organisations, and locations from text.
    """
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


def get_sentiment(text):
    """
    Sentiment analysis of text.
    """
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


def get_topics(tfidf_matrix, feature_names, n_top_words=10, model_type="NMF"):
    """
    Using LDA or NMF to identify the topics of interest.
    """
    if model_type == "NMF":
        model = NMF(n_components=5, random_state=1)
    else:
        model = LatentDirichletAllocation(n_components=5, random_state=1)

    model.fit(tfidf_matrix)

    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topics.append(
            [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        )

    return topics
