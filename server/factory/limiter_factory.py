from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

# Limiter configuration
limiter = Limiter(
    key_func=get_remote_address,  # Use the remote address of the client to limit rates
    storage_uri="redis://localhost:6379",  # Use a redis database
    default_limits=["200 per day", "5000 per hour"],  # Global rate limits
)
