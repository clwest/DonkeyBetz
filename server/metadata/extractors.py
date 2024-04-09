from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

from bs4 import BeautifulSoup as Soup
import spacy

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

# Initialize Sumy LSA summarizer
summarizer = LsaSummarizer()

def extract_title(html_content):
    soup = Soup(html_content, "html.parser")
    title_tag = soup.find("h1") or soup.find("title")  # Look for h1 or title tags
    return title_tag.string if title_tag else "Unknown Title"

def extract_keywords(html_content, keyword_tags=["h1", "h2", "h3"]):
    soup = Soup(html_content, "html.parser")
    keywords = [tag.string for tag in soup.find_all(keyword_tags)]
    return keywords

def extract_summary_from_text(text, sentence_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def generate_metadata(document):
    # Generate summary using Sumy LSA
    summary = extract_summary_from_text(document, sentence_count=5)
    
    # Generate keywords using spaCy
    doc = nlp(document)
    keywords = [chunk.text for chunk in doc.noun_chunks]
    
    # Create metadata dictionary
    metadata = {
        'summary': summary,
        'keywords': keywords
    }
    
    return metadata