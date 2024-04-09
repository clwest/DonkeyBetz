from datetime import datetime, timedelta
from pprint import pprint
import pytz
import uuid
from models.users import CustomMessage, ConversationSession, ConversationStatus
import helpers.helper_functions as hf
from factory import db

# Define the duration of inactivity after which a new session should start
SESSION_TIMEOUT = timedelta(minutes=30)


def get_or_create_session(user_id, topic_name=None):
    try:
        # Check if a topic name is provided
        if topic_name:
            # Handle conversation sessions with specific topic
            session = ConversationSession.query.filter_by(
                user_id=user_id, topic_name=topic_name
            ).first()

            if session:
                # Session exists return ID
                print(f"Existing session found: {session.id}")
                return session.id
            else:
                # Create new session
                print(f"Creating a new session...")
                new_session = ConversationSession(
                    user_id=user_id,
                    topic_name=topic_name,
                    conversation_status=ConversationStatus.ACTIVE,
                    last_accessed=datetime.utcnow(),
                )
                hf.add_to_db(new_session)
                db.session.commit()
                print(f"New Session ID: {new_session.id}")
                return new_session.id
        else:
            # Handle general session creation based on message timing
            last_message = (
                CustomMessage.query.filter_by(user_id=user_id)
                .order_by(CustomMessage.created_at.desc())
                .first()
            )

            if last_message and last_message.created_at:
                current_time = datetime.utcnow().replace(tzinfo=pytz.utc)
                time_diff = current_time - last_message.created_at

                if time_diff < SESSION_TIMEOUT:
                    return last_message.session_id
                else:
                    return str(uuid.uuid4())  # Start a new session
            else:
                return str(uuid.uuid4())  # Start a new session
    except Exception as e:
        print(f"Error in get_or_create_session: {e}")
        db.session.rollback()
