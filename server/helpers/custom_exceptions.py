


class NotFoundError(Exception):
    def __init__(self, message, status_code=404):
        super().__init__(message)
        self.status_code = status_code

class ForbiddenError(Exception):
    def __init__(self, message, status_code=403):
        super().__init__(message)
        self.status_code = status_code

class ValidationError(Exception):
    def __init__(self, message="Invalid request: Missing required fields.", status_code=404):
        self.message = message
        super().__init__(self.message)


class CategoryNotFoundError(Exception):
    def __init__(self, message="Category does not exist: The category_id provided does not correspond to any existing category.", status_code=404):
        super().__init__(message)
        self.status_code = status_code

class RateLimitExceededError(Exception):
    def __init__(self, message="Rate limit exceeded: You have exceeded the maximum number of requests per minute.", status_code=429):
        super().__init__(message)
        self.status_code = status_code

class UnauthorizedError(Exception):
    def __init__(self, message="Unauthorized: You do not have permission to perform this action.", status_code=403):
        super().__init__(message)
        self.status_code = status_code

class InternalServerError(Exception):
    def __init__(self, message="Internal Server Error: An unexpected error occurred. Please try again later.", status_code=500):
        super().__init__(message)
        self.status_code = status_code

class DataValidationError(Exception):
    def __init__(self, message="Data validation failed: One or more fields contain invalid data.", status_code=400):
        super().__init__(message)
        self.status_code = status_code

class UserAlreadyExistsError(Exception):
    def __init__(self, message="User already exists.", status_code=400):
        super().__init__(message)
        self.status_code = status_code

class UserNotFoundError(Exception):
    def __init__(self, message="User not found: The user could not be found.", status_code=404):
        super().__init__(message)
        self.status_code = status_code

class TokenBlacklistError(Exception):
    def __init__(self, message="Token is blacklisted.", status_code=403):
        super().__init__(message)
        self.status_code = status_code

class InvalidCredentialsError(Exception):
    def __init__(self, message="Invalid credentials.", status_code=401):
        super().__init__(message)
        self.status_code = status_code

class BadRequestError(Exception):
    def __init__(self, message="Bad Request.", status_code=400):
        super().__init__(message)
        self.status_code = status_code

class ResourceNotFoundError(Exception):
    """Raised when a requested resource is not found."""
    def __init__(self, message="Resource not found: The requested resource could not be found.", status_code=404):
        super().__init__(message)
        self.status_code = status_code
        
class CoinGeckoAPIError(Exception):
    def __init__(self, message="CoinGecko API request failed.", status_code=400):
        super().__init__(message)
        self.status_code = status_code
