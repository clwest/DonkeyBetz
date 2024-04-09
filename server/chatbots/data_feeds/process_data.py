import os
from dotenv import load_dotenv
from chatbots.loaders.process_urls import ingest_urls
from chatbots.loaders.process_pdfs import ingest_pdfs
from chatbots.loaders.process_youtube import ingest_videos
from chatbots.embeddings import generate_embeddings


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("DEV_DATABASE_URL")

def process_content(content_type, content_data):
    processed_data = []

    if content_type == "url":
        processed_data = ingest_urls(content_data)
    elif content_type == "pdf":
        processed_data = ingest_pdfs(content_data)
    elif content_type == "videos":
        processed_data = ingest_videos(content_data)

    if processed_data:
        embeddings_count, vectorstore = generate_embeddings(
            process_data, OPENAI_API_KEY, CONNECTION_STRING, "dynamic_user_content"
        )
        print(f"Processed and stored {embeddings_count} embeddings.")

    else:
        print("No data processed")
    
    return processed_data

def handle_chat_interaction():
    # from factory import db
    from chatbots.retrieval.chat_retrieval import ChatRetrievalLLM
    from chatbots.managers.chatbot_manager import ChatbotManager
    from chatbots.managers.message_manager import ChatMessageManger

    try:
        user_id = get_jwt_identity()["id"]
        user = User.query.get(user_id)
        user_email = user.email
        data = request.get_json()
        query = data.get("query", "")
        topic_name = generate_topic_name(query, nlp)
        entities = extract_entities(query, nlp)
        session_id = get_or_create_conversation_session(user_id, query, "")
        connection_string = os.getenv("DEV_DATABASE_URL")
        collection_name = "fuel_network"

        # Initialize components
        chat_manager = ChatManager()
        chat_retrieval_system = ChatRetrievalLLM()
        custom_message_converter = CustomMessageConverter(author_email=user_email)
        message_history_manager = ChatMessageManger(
            session_id, connection_string, custom_message_converter
        )

        # Process query and generate response
        selected_prompt = chat_manager.run_query(query)
        combined_chat_history = message_history_manager.get_formatted_conversations()
        final_response = chat_retrieval_system.llm_query(
            selected_prompt, combined_chat_history, collection_name
        )

        # Generate a description of hte AI's response
        ai_response_description = generate_description(final_response.get("answer", ""))
        # updated_conversation = update_conversation_session(
        #     session_id, topic_name, ai_response_description
        # )

        # Store and manage history
        message_history_manager.add_user_message(query)
        message_history_manager.add_ai_message(final_response)

        response_data = {
            "question": query,
            "answer": final_response["answer"]
            if isinstance(final_response, dict)
            else final_response,
            "topic_name": topic_name,
            "entities": entities,
            "summary": ai_response_description,
            # "update": updated_conversation
            # "session_description": updated_session.description,
        }
        return response_data

    except Exception as e:
        logger.error(f"Error in chat retrieval: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500