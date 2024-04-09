import os
import requests
from pprint import pprint
import spacy
import PyPDF2
from langchain.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from metadata.transformers import *
from dotenv import load_dotenv
from services.logging_config import root_logger as logger

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
nlp = spacy.load("en_core_web_sm")


class Document:
    def __init__(self, content, metadata=None, lemmatized_text=None):
        self.page_content = content
        self.metadata = metadata or {"title": ""}
        self.lemmatized_text = lemmatized_text or content

    @property
    def title(self):
        return self.metadata.get("title", "No Title")


def ingest_pdfs(batch_pdfs, pdf_title, collection_name):
    """Process and ingest PDF documents"""

    processed_pdfs = []
    for file_path in batch_pdfs:
        try:
            loader = PDFPlumberLoader(
                file_path=file_path,
            )
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            pdf_list = loader.load_and_split(text_splitter)
            for pdf in pdf_list:
                processed_pdf = process_pdfs(
                    pdf, nlp, pdf.metadata, pdf_title, collection_name
                )
                processed_pdfs.append(processed_pdf)

        except requests.RequestException as e:
            pprint(f"Failed to fetch PDF from URL: {file_path}. Error: {e}")
            logger.error(f"Failed to fetch PDF from URL: {file_path}. Error: {e}")

    return processed_pdfs


def process_pdfs(pdf, nlp, metadata, pdf_title, collection_name):
    """Process individual PDF for metadata, content, and embeddings"""
    cleaned_text = clean_text(pdf.page_content)

    lemmatized_text = lemmatize_text(cleaned_text, nlp)
    title = metadata.get("title", "No Title")
    if title == "No Title":
        title = f"{pdf_title}, PDFs"
    metadata_dict = {"title": pdf_title, "collection": collection_name, "source_type": "pdf"}

    logger.debug(
        f"Processed PDF '{title}' with content length: {len(lemmatized_text)} characters"
    )

    processed_data = Document(content=lemmatized_text, metadata=metadata_dict)
    return processed_data


if __name__ == "__main__":
    ingest_pdfs()
