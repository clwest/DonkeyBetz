import os
import re
from textwrap import shorten
from datetime import datetime
import spacy
import warnings
from models.chatbots import ConversationSession, ConversationStatus
import helpers.helper_functions as hf
from factory import db
from metadata.transformers import *
from services.logging_config import root_logger as logger

# Suppress only the specific warning from BeautifulSoup
warnings.filterwarnings("ignore", category=Warning)

nlp = spacy.load("en_core_web_sm")


def extract_topic_from_query(query):
    # Simplistic approach: use the first few words or apply more complex logic
    words = query.split()
    if len(words) > 3:
        topic = " ".join(words[:3]) + "..."
    else:
        topic = query
    return topic


def extract_description_from_response(response):
    # Extract the first sentence or a fixed length summary
    first_sentence = re.split(r"(?<=[.!?]) +", response)[0]
    return shorten(first_sentence, width=100, placeholder="...")


def get_or_create_conversation_session(user_id, query, response):
    try:
        topic_name = generate_topic_name(query, nlp)
        response_text = (
            response.get("answer", "") if isinstance(response, dict) else response
        )
        description = generate_description(response_text)

        session = ConversationSession.query.filter_by(
            user_id=user_id, topic_name=topic_name
        ).first()

        if session:
            # Update last accessed and return existing session ID
            session.last_accessed = datetime.utcnow()
            db.session.commit()
            logger.info(f"Updated existing session with ID {session.id}")
            return session.id
        else:
            # Create new session
            new_session = ConversationSession(
                user_id=user_id,
                topic_name=topic_name,
                description=description,
                conversation_status=ConversationStatus.ACTIVE,
                last_accessed=datetime.utcnow(),
            )
            db.session.add(new_session)
            db.session.commit()
            logger.info(f"Added session to the database {new_session.id}")
            return new_session.id
    except Exception as e:
        logger.error(f"Error in creating or retrieving conversation session: {e}")
        db.session.rollback()


def generate_topic_name(query, nlp):
    """
    Generates a topic name based on the named entities extracted from the query.

    Args:
        query (str): The user input or query from which to generate the topic name.
        nlp: The spaCy language model used for entity extraction.

    Returns:
        str: A string representing the topic name, derived from entities in the query.
            Falls back to a simplistic approach using the first few words of the query if no entities are found.

    This function aims to create a more meaningful and context-aware topic name by utilizing NLP entity extraction.
    If no significant entities are found, it defaults to using the initial words of the query.
    """

    if not isinstance(query, str):
        logger.debug(f"Non-string query received: {type(query)} - {query}")
        return "Default Topic"
    terms = extract_entities(query, nlp)
    topic_name = ", ".join(terms) if terms else query[:30]
    logger.info(f"Generating topic name: {topic_name}")
    return topic_name


def extract_entities(query, nlp):
    """
    Extracts named entities from a given query using spaCy NLP.

    Args:
        query (str): The user input or query from which to extract entities.
        nlp: The spaCy language model instance.

    Returns:
        list: A list of tuples, each containing the text and label of an extracted entity.

    This function is useful for identifying specific names, places, dates, or other unique identifiers in the query.
    """
    doc = nlp(query)
    entities = [
        entity.text for entity in doc.ents if entity.label_ in ["ORG", "PRODUCT"]
    ]
    noun_chunks = [
        chunk.text
        for chunk in doc.noun_chunks
        if chunk.root.pos_ in ["NOUN", "PROPN"] and chunk.text not in entities
    ]

    combined_terms = list(set(entities + noun_chunks))
    logger.info(f"Entities for topic extracted: {combined_terms}")
    return combined_terms


def generate_description(text):
    # Ensure text is a string and not empty
    if not isinstance(text, str) or not text.strip():
        logger.warning(f"Generate description received empty or invalid text: '{text}'")
        return "No description available due to inadequate text."

    try:
        logger.debug(f"Generating description for response: {text}")
        tfidf_matrix, feature_names = tfidf_transform([text])
        topics = get_topics(tfidf_matrix, feature_names)
        sentiment = get_sentiment(text)
        sentiment_desc = (
            "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        )
        result = f"Topics: {', '.join(topics[0])}. Sentiment: {sentiment_desc}."
        logger.debug(f"Generated description: {result}")
        return result
    except Exception as e:
        logger.error(f"Error during TF-IDF transformation: {e}")
        return "No description available due to processing error."


def update_conversation_session(session_id, topic_name, description):
    try:
        # Fetch Session ID
        session = ConversationSession.query.get(session_id)

        if session:
            # Update the session with the new topic name and description
            session.topic_name = topic_name
            session.description = description
            session.last_accessed = datetime.utcnow()

            # Save session to DB
            db.session.add(session)
            db.session.commit()

            return session
        else:
            raise ValueError(f"Session with ID {session_id} not found")
            return None

    except Exception as e:
        logger.error(f"Error updating conversation session: {e}")
        db.session.rollback()
        return None  # Reraise exception to handle it in the calling function
